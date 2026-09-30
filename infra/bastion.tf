# On-demand way in to the private database for a person with psql: a tiny instance reached
# through SSM Session Manager (no SSH, no public IP, no inbound rules). It joins the Lambdas'
# security group, which the database and the endpoints already accept, so no rule changes.
# Off by default; it costs about $25 a month while on (instance plus three endpoints).

locals {
  db_access_endpoints = var.enable_db_access ? toset(["ssm", "ssmmessages", "ec2messages"]) : toset([])
}

# The VPC has no internet, so the Session Manager agent reaches AWS through these. They share
# the SNS endpoint's security group, which already admits 443 from the Lambda group.
resource "aws_vpc_endpoint" "db_access" {
  for_each            = local.db_access_endpoints
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${data.aws_region.current.region}.${each.key}"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [aws_subnet.private[0].id]
  security_group_ids  = [aws_security_group.sns_endpoint.id]
  private_dns_enabled = true

  tags = { Name = "${var.name}-${each.key}" }
}

data "aws_ami" "al2023" {
  count       = var.enable_db_access ? 1 : 0
  owners      = ["amazon"]
  most_recent = true

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-kernel-*-arm64"]
  }
}

data "aws_iam_policy_document" "ec2_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "bastion" {
  count              = var.enable_db_access ? 1 : 0
  name               = "${var.name}-bastion"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json
}

resource "aws_iam_role_policy_attachment" "bastion_ssm" {
  count      = var.enable_db_access ? 1 : 0
  role       = aws_iam_role.bastion[0].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "bastion" {
  count = var.enable_db_access ? 1 : 0
  name  = "${var.name}-bastion"
  role  = aws_iam_role.bastion[0].name
}

resource "aws_instance" "bastion" {
  count                  = var.enable_db_access ? 1 : 0
  ami                    = data.aws_ami.al2023[0].id
  instance_type          = "t4g.nano"
  subnet_id              = aws_subnet.private[0].id
  vpc_security_group_ids = [aws_security_group.lambda.id]
  iam_instance_profile   = aws_iam_instance_profile.bastion[0].name

  metadata_options {
    http_tokens = "required"
  }

  root_block_device {
    volume_type = "gp3"
    encrypted   = true
  }

  tags = { Name = "${var.name}-bastion" }

  # A newer AMI must not replace a running bastion on every deploy.
  lifecycle {
    ignore_changes = [ami]
  }

  depends_on = [aws_vpc_endpoint.db_access, aws_iam_role_policy_attachment.bastion_ssm]
}
