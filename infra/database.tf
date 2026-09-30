# Letters and digits only: RDS rejects several punctuation characters in master passwords.
resource "random_password" "db" {
  length  = 32
  special = false
}

resource "aws_db_subnet_group" "feedback" {
  name       = var.name
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_db_instance" "feedback" {
  identifier     = var.name
  engine         = "postgres"
  engine_version = var.postgres_version
  instance_class = var.db_instance_class

  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = "feedback"
  username = "feedback_admin"
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.feedback.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false
  multi_az               = false

  auto_minor_version_upgrade = true
  backup_retention_period    = 7
  apply_immediately          = true

  # The table is the only copy of unsent feedback: a destroy must be deliberate.
  deletion_protection       = true
  skip_final_snapshot       = false
  final_snapshot_identifier = "${var.name}-final"
}
