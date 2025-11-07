#!/bin/bash
# Setup script for initial AWS infrastructure

set -e

AWS_REGION=${AWS_REGION:-us-east-1}
STACK_NAME=txtai-rag-infrastructure

echo "🏗️  Setting up AWS infrastructure..."

# Check if stack exists
if aws cloudformation describe-stacks --stack-name ${STACK_NAME} --region ${AWS_REGION} > /dev/null 2>&1; then
    echo "📝 Stack exists, updating..."
    aws cloudformation update-stack \
        --stack-name ${STACK_NAME} \
        --template-body file://deployment/aws/cloudformation-infrastructure.yaml \
        --parameters ParameterKey=VpcId,ParameterValue=vpc-xxxxxxxxx \
                     ParameterKey=SubnetIds,ParameterValue=subnet-xxxxxxxxx,subnet-yyyyyyyyy \
        --capabilities CAPABILITY_NAMED_IAM \
        --region ${AWS_REGION}
    
    echo "⏳ Waiting for stack update..."
    aws cloudformation wait stack-update-complete \
        --stack-name ${STACK_NAME} \
        --region ${AWS_REGION}
else
    echo "🆕 Creating new stack..."
    aws cloudformation create-stack \
        --stack-name ${STACK_NAME} \
        --template-body file://deployment/aws/cloudformation-infrastructure.yaml \
        --parameters ParameterKey=VpcId,ParameterValue=vpc-xxxxxxxxx \
                     ParameterKey=SubnetIds,ParameterValue=subnet-xxxxxxxxx,subnet-yyyyyyyyy \
        --capabilities CAPABILITY_NAMED_IAM \
        --region ${AWS_REGION}
    
    echo "⏳ Waiting for stack creation..."
    aws cloudformation wait stack-create-complete \
        --stack-name ${STACK_NAME} \
        --region ${AWS_REGION}
fi

echo "✅ Infrastructure setup complete!"

# Get outputs
echo "📋 Stack outputs:"
aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query 'Stacks[0].Outputs' \
    --output table

