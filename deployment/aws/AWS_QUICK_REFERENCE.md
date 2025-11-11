# Quick Reference: AWS Commands with Profile

Since you're using AWS SSO, remember to use the `--profile` flag or set `AWS_PROFILE`:

## Set Default Profile (Optional)

```bash
export AWS_PROFILE=rays-admin-profile
```

## Common Commands

```bash
# Login to SSO (when credentials expire)
aws sso login --profile rays-admin-profile

# Verify credentials
aws sts get-caller-identity --profile rays-admin-profile

# List ECR repositories
aws ecr describe-repositories --region us-east-1 --profile rays-admin-profile

# Get Docker login token
aws ecr get-login-password --region us-east-1 --profile rays-admin-profile | \
  docker login --username AWS --password-stdin 076656108307.dkr.ecr.us-east-1.amazonaws.com
```

## Your ECR Repositories

- **Backend**: `076656108307.dkr.ecr.us-east-1.amazonaws.com/txtai-rag-backend`
- **Frontend**: `076656108307.dkr.ecr.us-east-1.amazonaws.com/txtai-rag-frontend`

## Next Steps

1. ✅ ECR repositories created
2. ⏭️ Create IAM roles (ecsTaskExecutionRole, ecsTaskRole)
3. ⏭️ Setup infrastructure (CloudFormation)
4. ⏭️ Deploy services

See `deployment/DEPLOYMENT.md` for detailed instructions.

