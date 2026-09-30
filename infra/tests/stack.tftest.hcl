# Checks the stack's wiring without AWS: the provider is mocked, so this runs anywhere.
# Needs feedback-service/dist/feedback-service.zip (npm run package) to exist.

mock_provider "aws" {
  # The provider validates ARNs even when mocked, so generated values must look like ARNs.
  mock_resource "aws_iam_role" {
    defaults = { arn = "arn:aws:iam::123456789012:role/mock" }
  }
  mock_resource "aws_sns_topic" {
    defaults = { arn = "arn:aws:sns:us-east-1:123456789012:mock" }
  }
  mock_resource "aws_lambda_function" {
    defaults = { arn = "arn:aws:lambda:us-east-1:123456789012:function:mock" }
  }

  override_data {
    target = data.aws_availability_zones.available
    values = { names = ["zone-a", "zone-b"] }
  }
  override_data {
    target = data.aws_region.current
    values = { region = "us-east-1" }
  }
  override_data {
    target = data.aws_caller_identity.current
    values = { account_id = "123456789012" }
  }
  override_data {
    target = data.aws_iam_policy_document.lambda_assume
    values = { json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}" }
  }
  override_data {
    target = data.aws_iam_policy_document.scheduler_assume
    values = { json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}" }
  }
}

mock_provider "random" {}

variables {
  notify_email = "owner@example.com"
}

run "stack" {
  command = apply

  assert {
    condition     = aws_scheduler_schedule.digest.schedule_expression == "cron(0 20 * * ? *)" && aws_scheduler_schedule.digest.schedule_expression_timezone == "America/Chicago"
    error_message = "The digest must run at 20:00 America/Chicago, as config.json says."
  }

  assert {
    condition     = aws_lambda_function.fn["submit"].reserved_concurrent_executions == 2 && aws_lambda_function.fn["digest"].reserved_concurrent_executions == -1
    error_message = "Only the submit Lambda is capped."
  }

  assert {
    condition     = contains(keys(aws_lambda_function.fn["digest"].environment[0].variables), "TOPIC_ARN") && !contains(keys(aws_lambda_function.fn["submit"].environment[0].variables), "TOPIC_ARN")
    error_message = "Only the digest Lambda gets the topic."
  }

  assert {
    condition     = alltrue([for f in aws_lambda_function.fn : f.environment[0].variables.PGDATABASE == "feedback" && f.environment[0].variables.PGUSER == "feedback_admin"])
    error_message = "Every Lambda must be pointed at the feedback database."
  }

  assert {
    condition     = aws_lambda_function.fn["submit"].handler == "submit.handler" && aws_lambda_function.fn["digest"].handler == "digest.handler" && aws_lambda_function.fn["migrate"].handler == "migrate.handler"
    error_message = "Handlers must match the files in feedback-service/."
  }

  assert {
    condition     = aws_lambda_function_url.submit.authorization_type == "NONE" && aws_lambda_function_url.submit.cors[0].allow_origins == toset(["https://vishalkhopkar.github.io"])
    error_message = "The submit URL must be public but only accept the site's origin."
  }

  assert {
    condition     = aws_lambda_permission.submit_url.function_url_auth_type == "NONE" && aws_lambda_permission.submit_url_invoke.invoked_via_function_url == true
    error_message = "Both function URL permission statements are needed, or every request gets 403."
  }

  assert {
    condition     = aws_db_instance.feedback.publicly_accessible == false && aws_db_instance.feedback.deletion_protection == true && aws_db_instance.feedback.storage_encrypted == true
    error_message = "The database must be private, encrypted and protected from deletion."
  }

  assert {
    condition     = aws_vpc_endpoint.sns.service_name == "com.amazonaws.us-east-1.sns" && aws_vpc_endpoint.sns.private_dns_enabled == true
    error_message = "The digest Lambda reaches SNS only through the endpoint's private DNS."
  }

  assert {
    condition     = alltrue([for g in aws_cloudwatch_log_group.fn : g.retention_in_days == 90])
    error_message = "Logs hold personal data and must expire."
  }
}

run "no_concurrency_headroom" {
  command = plan

  variables {
    submit_reserved_concurrency = -1
  }

  assert {
    condition     = aws_lambda_function.fn["submit"].reserved_concurrent_executions == -1
    error_message = "The workflow's fallback for accounts limited to 10 concurrent executions must reach the function."
  }
}
