# Project Structure

```
ragaws/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Application configuration
│   │   │   ├── txtai_client.py     # txtai embeddings client
│   │   │   ├── bedrock_client.py   # AWS Bedrock client
│   │   │   └── document_processor.py # PDF/Markdown processing
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── ingestion.py        # Document upload & indexing
│   │       ├── retrieval.py        # Semantic search (decoupled)
│   │       └── generation.py        # LLM generation (decoupled)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadSection.jsx   # Document upload UI
│   │   │   ├── QuerySection.jsx    # Query input UI
│   │   │   └── ResultsSection.jsx  # Results display
│   │   ├── App.jsx                 # Main app component
│   │   ├── main.jsx                # React entry point
│   │   └── index.css               # Global styles (black/white theme)
│   ├── Dockerfile
│   ├── nginx.conf                  # Nginx config for production
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example
│
├── deployment/
│   ├── aws/
│   │   ├── ecs-backend-task-definition.json    # ECS task definition
│   │   ├── ecs-frontend-task-definition.json
│   │   ├── ecs-backend-service.json            # ECS service config
│   │   ├── ecs-frontend-service.json
│   │   ├── cloudformation-infrastructure.yaml  # Infrastructure as code
│   │   ├── iam-ecs-task-execution-role-policy.json
│   │   ├── iam-ecs-task-role-policy.json
│   │   ├── deploy.sh                           # Deployment script
│   │   └── setup-infrastructure.sh             # Infrastructure setup
│   └── DEPLOYMENT.md                           # Deployment guide
│
├── docker-compose.yml              # Local development stack
├── Makefile                        # Convenience commands
├── README.md                       # Main documentation
├── DEVELOPMENT.md                  # Development guide
├── CONTRIBUTING.md                 # Contribution guidelines
└── .gitignore                      # Git ignore rules
```

## Key Components

### Backend Layers (Decoupled)

1. **Ingestion Layer** (`routers/ingestion.py`)
   - Document upload (PDF, Markdown)
   - Text extraction and chunking
   - txtai embedding indexing

2. **Retrieval Layer** (`routers/retrieval.py`)
   - Semantic search using txtai
   - Returns relevant context chunks
   - **Decoupled from generation**

3. **Generation Layer** (`routers/generation.py`)
   - AWS Bedrock integration
   - Supports Claude, Titan, Llama models
   - **Decoupled from retrieval**

### Frontend Components

- **UploadSection**: File upload with drag-and-drop
- **QuerySection**: Query input with submit button
- **ResultsSection**: Displays retrieved chunks and LLM response

### AWS Infrastructure

- **ECS Fargate**: Container orchestration
- **EFS**: Persistent storage for txtai index
- **CloudFormation**: Infrastructure as code
- **IAM Roles**: Secure access to AWS services

