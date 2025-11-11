#!/bin/bash
# Quick reference for common commands

echo "📋 Quick Reference"
echo "=================="
echo ""

echo "🔐 AWS Commands (use --profile flag):"
echo "  aws sso login --profile rays-admin-profile"
echo "  aws ecr describe-repositories --region us-east-1 --profile rays-admin-profile"
echo ""

echo "🐍 Backend Commands:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""

echo "⚛️  Frontend Commands:"
echo "  cd frontend"
echo "  npm install"
echo "  npm run dev"
echo ""

echo "🐳 Docker Commands:"
echo "  docker-compose up --build"
echo ""

echo "📝 Note: Always use --profile rays-admin-profile for AWS commands"
echo "   or set: export AWS_PROFILE=rays-admin-profile"

