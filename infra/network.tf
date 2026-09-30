# A VPC of its own with two private subnets and no internet gateway or NAT: the Lambdas reach
# the database directly and SNS through an interface endpoint, and nothing else.

data "aws_availability_zones" "available" {
  state = "available"
  # Lambda cannot attach to use1-az3 in us-east-1.
  exclude_zone_ids = ["use1-az3"]
}

resource "aws_vpc" "main" {
  cidr_block           = "10.60.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true # needed for the SNS endpoint's private DNS

  tags = { Name = var.name }
}

# RDS requires subnets in two availability zones.
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 1)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = { Name = "${var.name}-private-${count.index + 1}" }
}

resource "aws_security_group" "lambda" {
  name        = "${var.name}-lambda"
  description = "Feedback Lambdas"
  vpc_id      = aws_vpc.main.id
}

resource "aws_security_group" "db" {
  name        = "${var.name}-db"
  description = "Feedback database"
  vpc_id      = aws_vpc.main.id
}

resource "aws_security_group" "sns_endpoint" {
  name        = "${var.name}-sns-endpoint"
  description = "SNS interface endpoint"
  vpc_id      = aws_vpc.main.id
}

resource "aws_vpc_security_group_egress_rule" "lambda_to_db" {
  security_group_id            = aws_security_group.lambda.id
  referenced_security_group_id = aws_security_group.db.id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
}

resource "aws_vpc_security_group_egress_rule" "lambda_to_sns" {
  security_group_id            = aws_security_group.lambda.id
  referenced_security_group_id = aws_security_group.sns_endpoint.id
  ip_protocol                  = "tcp"
  from_port                    = 443
  to_port                      = 443
}

resource "aws_vpc_security_group_ingress_rule" "db_from_lambda" {
  security_group_id            = aws_security_group.db.id
  referenced_security_group_id = aws_security_group.lambda.id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
}

resource "aws_vpc_security_group_ingress_rule" "sns_from_lambda" {
  security_group_id            = aws_security_group.sns_endpoint.id
  referenced_security_group_id = aws_security_group.lambda.id
  ip_protocol                  = "tcp"
  from_port                    = 443
  to_port                      = 443
}

# Only the digest Lambda publishes to SNS. One subnet is enough, and each extra subnet adds
# about $7 a month.
resource "aws_vpc_endpoint" "sns" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${data.aws_region.current.region}.sns"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [aws_subnet.private[0].id]
  security_group_ids  = [aws_security_group.sns_endpoint.id]
  private_dns_enabled = true

  tags = { Name = "${var.name}-sns" }
}
