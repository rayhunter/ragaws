# AWS Deployment Guide

This guide walks you through deploying the txtai RAG system to AWS ECS.

## Prerequisites

1. AWS CLI installed and configured
2. AWS account with appropriate permissions
3. Docker installed locally
4. ECR repositories created (or use the script below)

## Step 1: Create ECR Repositories

```bash
aws ecr create-repository --repository-name txtai-rag-backend --region us-east-1
aws ecr create-repository --repository-name txtai-rag-frontend --region us-east-1
```

## Step 2: Create IAM Roles

### Task Execution Role

This role allows ECS to pull images and write logs:

```bash
# Create role
aws iam create-role \
  --role-name ecsTaskExecutionRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ecs-tasks.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policy
aws iam put-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-name EcsTaskExecutionRolePolicy \
  --policy-document file://deployment/aws/iam-ecs-task-execution-role-policy.json
```

### Task Role

This role allows the application to access Bedrock, S3, DynamoDB, and EFS:

```bash
# Create role
aws iam create-role \
  --role-name ecsTaskRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ecs-tasks.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policy
aws iam put-role-policy \
  --role-name ecsTaskRole \
  --policy-name EcsTaskRolePolicy \
  --policy-document file://deployment/aws/iam-ecs-task-role-policy.json
```

## Step 3: Setup Infrastructure

Update `deployment/aws/cloudformation-infrastructure.yaml` with your VPC and subnet IDs, then run:

```bash
cd deployment/aws
./setup-infrastructure.sh
```

This creates:
- ECS Cluster
- EFS File System (for txtai index persistence)
- Security Groups
- CloudWatch Log Groups

## Step 4: Update Task Definitions

Before deploying, update these placeholders in the task definition files:

1. **ecs-backend-task-definition.json**:
   - Replace `YOUR_ACCOUNT_ID` with your AWS account ID
   - Replace `YOUR_EFS_FILE_SYSTEM_ID` with EFS ID from CloudFormation output
   - Replace `YOUR_EFS_ACCESS_POINT_ID` with EFS Access Point ID from CloudFormation output
   - Update subnet IDs and security group IDs

2. **ecs-frontend-task-definition.json**:
   - Replace `YOUR_ACCOUNT_ID` with your AWS account ID
   - Update `VITE_API_URL` with your API Gateway or ALB URL

3. **ecs-backend-service.json** and **ecs-frontend-service.json**:
   - Update subnet IDs
   - Update security group IDs
   - Update target group ARNs (if using ALB)

## Step 5: Create Application Load Balancer (Optional but Recommended)

If you want to use an ALB:

```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name txtai-rag-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx \
  --region us-east-1

# Create target groups
aws elbv2 create-target-group \
  --name txtai-backend-tg \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxx \
  --target-type ip \
  --health-check-path /health

aws elbv2 create-target-group \
  --name txtai-frontend-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-xxx \
  --target-type ip \
  --health-check-path /
```

## Step 6: Deploy

```bash
# Set your AWS account ID
export AWS_ACCOUNT_ID=123456789012

# Run deployment script
cd deployment/aws
./deploy.sh
```

## Step 7: Verify Deployment

```bash
# Check service status
aws ecs describe-services \
  --cluster txtai-rag-cluster \
  --services txtai-rag-backend-service txtai-rag-frontend-service \
  --region us-east-1

# Check task status
aws ecs list-tasks \
  --cluster txtai-rag-cluster \
  --service-name txtai-rag-backend-service \
  --region us-east-1
```

## Step 8: Access the Application

Once deployed, access the frontend via:
- ALB DNS name (if using ALB)
- ECS service public IP (if public IP enabled)
- CloudFront distribution (if configured)

## Troubleshooting

### Check Logs

```bash
# Backend logs
aws logs tail /ecs/txtai-rag-backend --follow --region us-east-1

# Frontend logs
aws logs tail /ecs/txtai-rag-frontend --follow --region us-east-1
```

### Common Issues

1. **Tasks failing to start**: Check IAM roles and security groups
2. **EFS mount issues**: Verify EFS access point and security group rules
3. **Bedrock access denied**: Ensure task role has Bedrock permissions
4. **Image pull errors**: Verify ECR repository exists and task execution role has permissions

## Scaling

### Auto Scaling

Create auto-scaling configuration:

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/txtai-rag-cluster/txtai-rag-backend-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/txtai-rag-cluster/txtai-rag-backend-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-scaling-policy \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
    }
  }'
```

## Cost Optimization

- Use Fargate Spot for non-critical workloads
- Set up CloudWatch alarms for cost monitoring
- Configure EFS lifecycle policies for old indexes
- Use S3 Intelligent-Tiering for document storage

