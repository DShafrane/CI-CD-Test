provider "aws" {
  version = "~> 2.0"
  region  = "var.region"
  #shared_credentials_file = "$HOME/.aws/credentials"
  #access_key = var.access_key
  #secret_key = var.secret_key
}

resource "random_string" "flask-secret-key" {
  length = 16
  special = true
  override_special = "/@\" "
}
