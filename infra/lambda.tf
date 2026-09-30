locals {
  service_dir = "${path.module}/../feedback-service"
  # Built by `npm run package` in feedback-service/ before Terraform runs.
  bundle = "${local.service_dir}/dist/feedback-service.zip"

  db_env = {
    PGHOST     = aws_db_instance.feedback.address
    PGPORT     = tostring(aws_db_instance.feedback.port)
    PGDATABASE = aws_db_instance.feedback.db_name
    PGUSER     = aws_db_instance.feedback.username
    PGPASSWORD = random_password.db.result
  }

  functions = {
    submit  = { handler = "submit.handler", timeout = 10, role = aws_iam_role.lambda.arn }
    digest  = { handler = "digest.handler", timeout = 60, role = aws_iam_role.digest.arn }
    migrate = { handler = "migrate.handler", timeout = 30, role = aws_iam_role.lambda.arn }
  }
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# submit and migrate: logs and VPC networking only.
resource "aws_iam_role" "lambda" {
  name               = "${var.name}-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# digest: the same, plus publishing to the feedback topic.
resource "aws_iam_role" "digest" {
  name               = "${var.name}-digest"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy_attachment" "digest_vpc" {
  role       = aws_iam_role.digest.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy" "digest_publish" {
  name = "publish-feedback-digest"
  role = aws_iam_role.digest.id
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sns:Publish", Resource = aws_sns_topic.feedback.arn }]
  })
}

resource "aws_cloudwatch_log_group" "fn" {
  for_each          = local.functions
  name              = "/aws/lambda/${var.name}-${each.key}"
  retention_in_days = var.log_retention_days
}

resource "aws_lambda_function" "fn" {
  for_each = local.functions

  function_name    = "${var.name}-${each.key}"
  role             = each.value.role
  runtime          = "nodejs22.x"
  architectures    = ["arm64"]
  handler          = each.value.handler
  filename         = local.bundle
  source_code_hash = filebase64sha256(local.bundle)
  timeout          = each.value.timeout
  memory_size      = 256

  reserved_concurrent_executions = each.key == "submit" ? var.submit_reserved_concurrency : -1

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = merge(local.db_env, each.key == "digest" ? { TOPIC_ARN = aws_sns_topic.feedback.arn } : {})
  }

  depends_on = [
    aws_cloudwatch_log_group.fn,
    aws_iam_role_policy_attachment.lambda_vpc,
    aws_iam_role_policy_attachment.digest_vpc,
  ]
}

# ---------------------------------------------------------------- public submit endpoint

resource "aws_lambda_function_url" "submit" {
  function_name      = aws_lambda_function.fn["submit"].function_name
  authorization_type = "NONE"

  cors {
    allow_origins = [var.site_origin]
    allow_methods = ["POST"]
    allow_headers = ["content-type"]
    max_age       = 86400
  }
}

# Outside the console, a NONE-auth function URL needs both statements added explicitly, or
# every request is refused with 403. The second is limited to calls through the URL.
resource "aws_lambda_permission" "submit_url" {
  statement_id           = "FunctionURLAllowPublicAccess"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.fn["submit"].function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

resource "aws_lambda_permission" "submit_url_invoke" {
  statement_id             = "FunctionURLInvokeAllowPublicAccess"
  action                   = "lambda:InvokeFunction"
  function_name            = aws_lambda_function.fn["submit"].function_name
  principal                = "*"
  invoked_via_function_url = true
}

# ---------------------------------------------------------------- schema

# Creates the table on the first deploy and re-applies schema.sql whenever it changes. A
# failure here fails the apply.
resource "aws_lambda_invocation" "migrate" {
  function_name = aws_lambda_function.fn["migrate"].function_name
  input         = jsonencode({})

  triggers = {
    schema   = filesha256("${local.service_dir}/schema.sql")
    database = aws_db_instance.feedback.resource_id
  }

  depends_on = [
    aws_vpc_security_group_egress_rule.lambda_to_db,
    aws_vpc_security_group_ingress_rule.db_from_lambda,
  ]
}
