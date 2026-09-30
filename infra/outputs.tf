output "submit_url" {
  description = "Put this in config.js as feedbackEndpoint."
  value       = aws_lambda_function_url.submit.function_url
}

output "digest_schedule" {
  value = "${aws_scheduler_schedule.digest.schedule_expression} ${aws_scheduler_schedule.digest.schedule_expression_timezone}"
}

output "sns_topic_arn" {
  value = aws_sns_topic.feedback.arn
}

output "database_endpoint" {
  value = aws_db_instance.feedback.address
}
