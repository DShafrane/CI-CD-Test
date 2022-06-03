# Set up region
provider "aws" {
  version = "~> 2.0"
  region  = "us-east-1"
}

# Create ECR repository
resource "aws_ecr_repository" "Flask_app_repo" {
  name = "Flask_app_repo" # Naming my repository
}

# Create ECS cluster
resource "aws_ecs_cluster" "my_cluster" {
  name = "my-cluster" # Naming the cluster
}

# Create task
resource "aws_ecs_task_definition" "Flask_app_task" {
  family                   = "Flask_app_task" # Naming our first task
  container_definitions    = <<DEFINITION
  [
    {
      "name": "Flask_app_task",
      "image": "${aws_ecr_repository.Flask_app_repo.repository_url}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"] # Stating that we are using ECS Fargate
  network_mode             = "awsvpc"    # Using awsvpc as our network mode as this is required for Fargate
  memory                   = 512         # Specifying the memory our container requires
  cpu                      = 256         # Specifying the CPU our container requires
  execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole.arn}"
}

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy.json}"
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = "${aws_iam_role.ecsTaskExecutionRole.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
