# Fix Guide for Common Issues

## Issue 1: AWS Credentials Error

**Error**: `The security token included in the request is invalid`

**Solution**: Always use `--profile` flag with AWS commands:

```bash
# Option 1: Use --profile flag
aws ecr create-repository --repository-name txtai-rag-backend --region us-east-1 --profile rays-admin-profile

# Option 2: Set AWS_PROFILE environment variable
export AWS_PROFILE=rays-admin-profile
aws ecr create-repository --repository-name txtai-rag-backend --region us-east-1

# Option 3: Login to SSO first (if expired)
aws sso login --profile rays-admin-profile
```

## Issue 2: uvicorn Command Not Found

**Error**: `zsh: command not found: uvicorn`

**Solution**: Activate virtual environment first:

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

Or use the setup script:
```bash
cd backend
./setup.sh
source venv/bin/activate
uvicorn app.main:app --reload
```

## Issue 3: PyMuPDF Build Errors

**Error**: Compilation errors when installing PyMuPDF

**Solution**: We've switched to `pypdf` which is easier to install. If you still see errors:

```bash
cd backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Quick Fix Commands

```bash
# Fix AWS credentials
export AWS_PROFILE=rays-admin-profile
aws sso login --profile rays-admin-profile

# Fix backend setup
cd backend
./setup.sh
source venv/bin/activate
uvicorn app.main:app --reload

# Fix frontend setup
cd frontend
npm install
npm run dev
```

