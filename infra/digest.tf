locals {
  config = jsondecode(file("${local.service_dir}/config.json"))
  # config.json is the single source of the digest's time and zone: "20:00", "America/Chicago".
  digest_hour   = tonumber(split(":", local.config.digest.time)[0])
  digest_minute = tonumber(split(":", local.config.digest.time)[1])
}

resource "aws_sns_topic" "feedback" {
  name = var.name
}

# Stays "pending confirmation" until the link SNS emails to this address is clicked.
resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.feedback.arn
  protocol  = "email"
  endpoint  = var.notify_email
}

data "aws_iam_policy_document" "scheduler_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
  }
}

resource "aws_iam_role" "scheduler" {
  name               = "${var.name}-scheduler"
  assume_role_policy = data.aws_iam_policy_document.scheduler_assume.json
}

resource "aws_iam_role_policy" "scheduler_invoke" {
  name = "invoke-digest"
  role = aws_iam_role.scheduler.id
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "lambda:InvokeFunction", Resource = aws_lambda_function.fn["digest"].arn }]
  })
}

# Scheduler evaluates the cron in the given zone, so daylight saving is handled.
resource "aws_scheduler_schedule" "digest" {
  name                         = "${var.name}-digest"
  schedule_expression          = "cron(${local.digest_minute} ${local.digest_hour} * * ? *)"
  schedule_expression_timezone = local.config.digest.timezone

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.fn["digest"].arn
    role_arn = aws_iam_role.scheduler.arn

    retry_policy {
      maximum_retry_attempts = 2
    }
  }
}
