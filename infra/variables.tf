variable "name" {
  description = "Prefix for every resource's name."
  type        = string
  default     = "india-borders-feedback"
}

variable "notify_email" {
  description = "Address the nightly feedback digest is sent to. SNS mails a confirmation link to it first."
  type        = string
  sensitive   = true
}

variable "site_origin" {
  description = "The only browser origin allowed to post feedback (CORS)."
  type        = string
  default     = "https://vishalkhopkar.github.io"
}

variable "submit_reserved_concurrency" {
  description = "Most simultaneous submit Lambdas, the MVP rate limit. -1 for no limit (needed on accounts whose total concurrency is only 10)."
  type        = number
  default     = 2
}

variable "db_instance_class" {
  type    = string
  default = "db.t4g.micro"
}

variable "postgres_version" {
  description = "Major version; RDS applies minor upgrades itself."
  type        = string
  default     = "17"
}

variable "log_retention_days" {
  description = "The submit log holds messages, email addresses and IPs, so it is not kept forever."
  type        = number
  default     = 90
}
