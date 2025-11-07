# txtai RAG System

Production-grade RAG (Retrieval-Augmented Generation) system built with **txtai**, **FastAPI**, **React**, and **AWS**.

## 🏗️ Architecture

```
React Frontend (Vite + TailwindCSS)
   ↓ REST API
FastAPI Backend
   ├── Ingestion Layer (txtai embeddings)
   ├── Retrieval Layer (semantic search)
   └── Generation Layer (AWS Bedrock - Claude/Titan/Llama)
```

## 📁 Project Structure

```
ragaws/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── core/          # Core modules (txtai, bedrock, config)
│   │   ├── routers/       # API routes (ingestion, retrieval, generation)
│   │   └── main.py        # FastAPI application
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   └── App.jsx
│   ├── Dockerfile
│   └── package.json
│
└── deployment/
    └── aws/              # AWS ECS deployment configs
        ├── ecs-*-task-definition.json
        ├── ecs-*-service.json
        └── cloudformation-infrastructure.yaml
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker
- AWS CLI configured
- AWS Bedrock access enabled

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables (copy .env.example to .env)
cp .env.example .env
# Edit .env with your AWS credentials

# Run backend
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install

# Set API URL (copy .env.example to .env)
cp .env.example .env
# Edit .env: VITE_API_URL=http://localhost:8000

# Run frontend
npm run dev
```

## ☁️ AWS Deployment

### 1. Create ECR Repositories

```bash
aws ecr create-repository --repository-name txtai-rag-backend --region us-east-1
aws ecr create-repository --repository-name txtai-rag-frontend --region us-east-1
```

### 2. Setup Infrastructure

```bash
cd deployment/aws
./setup-infrastructure.sh
```

### 3. Deploy Services

```bash
./deploy.sh
```

### 4. Update Task Definitions

Before deploying, update these placeholders in `deployment/aws/`:

- `YOUR_ACCOUNT_ID` - Your AWS account ID
- `YOUR_EFS_FILE_SYSTEM_ID` - EFS file system ID (from CloudFormation output)
- `YOUR_EFS_ACCESS_POINT_ID` - EFS access point ID (from CloudFormation output)
- `YOUR_API_GATEWAY_URL` - API Gateway URL (if using API Gateway)
- Subnet IDs and Security Group IDs

## 🔧 Configuration

### Backend Environment Variables

See `backend/.env.example`:

- `TXTAI_MODEL` - Embedding model (default: `sentence-transformers/all-MiniLM-L6-v2`)
- `BEDROCK_MODEL_ID` - Bedrock model (options: `anthropic.claude-v2`, `amazon.titan-text-lite-v1`, `meta.llama2-13b-chat-v1`)
- `AWS_REGION` - AWS region
- `TXTAI_INDEX_PATH` - Path for txtai index (use `/mnt/efs/txtai_index` for EFS)

### Frontend Environment Variables

See `frontend/.env.example`:

- `VITE_API_URL` - Backend API URL

## 📡 API Endpoints

### Ingestion

- `POST /api/v1/ingestion/upload` - Upload and index document
- `GET /api/v1/ingestion/stats` - Get index statistics

### Retrieval (Decoupled)

- `POST /api/v1/retrieval/query` - Retrieve relevant context chunks

### Generation (Decoupled)

- `POST /api/v1/generation/generate` - Generate LLM response
- `POST /api/v1/generation/rag` - Combined RAG pipeline
- `GET /api/v1/generation/models` - List available Bedrock models

## 🧩 Key Features

- ✅ **Decoupled Architecture** - Retrieval and generation are separate layers
- ✅ **AWS Bedrock Integration** - Supports Claude, Titan, and Llama models
- ✅ **Persistent Index** - txtai index stored on EFS for scalability
- ✅ **Production Ready** - ECS Fargate, auto-scaling, health checks
- ✅ **Black & White UI** - Clean, professional React interface

## 🔒 Security

- EFS encryption enabled
- Security groups configured
- IAM roles for ECS tasks
- HTTPS via Application Load Balancer

## 📊 Monitoring

- CloudWatch Logs: `/ecs/txtai-rag-backend` and `/ecs/txtai-rag-frontend`
- Container Insights enabled on ECS cluster
- Health checks configured for both services

## 🛠️ Development

### Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Building Docker Images

```bash
# Backend
cd backend
docker build -t txtai-rag-backend .

# Frontend
cd frontend
docker build -t txtai-rag-frontend .
```

## 📝 License

MIT

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions, please open a GitHub issue.

