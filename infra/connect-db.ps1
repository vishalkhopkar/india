# Opens psql on the private feedback database through the Session Manager bastion.
# Needs: AWS CLI v2, the Session Manager plugin, psql, AWS credentials (aws configure), and the
# bastion (repository variable ENABLE_DB_ACCESS=true, then rerun the Feedback service workflow).
#
#   .\infra\connect-db.ps1                      # interactive psql
#   .\infra\connect-db.ps1 -c "table feedback"  # anything after the named parameters goes to psql
param(
  [string]$Region = 'us-east-2',
  [string]$Name = 'india-borders-feedback',
  [int]$LocalPort = 5433,
  [Parameter(ValueFromRemainingArguments = $true)] [string[]]$PsqlArgs
)
$ErrorActionPreference = 'Stop'

function Aws([string[]]$a) {
  $out = & aws @a --region $Region --output text 2>&1
  if ($LASTEXITCODE -ne 0) { throw "aws $($a[0..1] -join ' ') failed: $out" }
  "$out".Trim()
}

$instance = Aws @('ec2', 'describe-instances',
  '--filters', "Name=tag:Name,Values=$Name-bastion", 'Name=instance-state-name,Values=running',
  '--query', 'Reservations[0].Instances[0].InstanceId')
if (-not $instance -or $instance -eq 'None') {
  throw 'No running bastion. Set the ENABLE_DB_ACCESS repository variable to true and rerun the Feedback service workflow.'
}
$dbHost = Aws @('rds', 'describe-db-instances', '--db-instance-identifier', $Name, '--query', 'DBInstances[0].Endpoint.Address')
# The password Terraform generated lives only in the Lambdas' configuration.
$env:PGPASSWORD = Aws @('lambda', 'get-function-configuration', '--function-name', "$Name-submit", '--query', 'Environment.Variables.PGPASSWORD')

$tunnel = Start-Process -FilePath (Get-Command aws).Source -PassThru -WindowStyle Hidden -ArgumentList @(
  'ssm', 'start-session', '--region', $Region, '--target', $instance,
  '--document-name', 'AWS-StartPortForwardingSessionToRemoteHost',
  '--parameters', "host=$dbHost,portNumber=5432,localPortNumber=$LocalPort")
try {
  $deadline = (Get-Date).AddSeconds(30)
  while (-not (Test-NetConnection 127.0.0.1 -Port $LocalPort -InformationLevel Quiet -WarningAction SilentlyContinue)) {
    if ($tunnel.HasExited -or (Get-Date) -gt $deadline) { throw 'The Session Manager tunnel did not open.' }
    Start-Sleep -Milliseconds 500
  }
  # hostaddr sends the connection into the tunnel; host keeps verify-full checking the real name.
  $ca = Join-Path $PSScriptRoot '..\feedback-service\global-bundle.pem'
  & psql "host=$dbHost hostaddr=127.0.0.1 port=$LocalPort dbname=feedback user=feedback_admin sslmode=verify-full sslrootcert=$ca" @PsqlArgs
} finally {
  if (-not $tunnel.HasExited) { Stop-Process -Id $tunnel.Id -Force }
  Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
}
