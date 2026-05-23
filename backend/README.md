# Banking AI-Agent — Backend (API Gateway)

FastAPI-based API Gateway that orchestrates the banking AI agentic workflow.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/config` | System configuration |
| POST | `/run-agent` | Execute full agentic workflow |

## Workflow Pipeline

```
Customer Message
    → Intent Detection (gRPC → Intent Service)
    → Priority Assessment (rule-based)
    → Policy Retrieval (lookup)
    → Validation (checks)
    → Routing (department mapping)
    → Draft Generation (Ollama HTTP)
    → Structured Response
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `INTENT_SERVICE_HOST` | `localhost` | Intent Service hostname |
| `INTENT_SERVICE_PORT` | `50051` | Intent Service gRPC port |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API URL |
| `OLLAMA_MODEL_NAME` | `gpt-oss:20b` | Ollama model name |
| `OLLAMA_TIMEOUT` | `120.0` | Ollama request timeout (seconds) |

## Running Locally

```bash
pip install -r requirements.txt
cd app/clients/intent_grpc && make && cd ../../..
python run.py
```

## Docker

```bash
docker build -t banking-backend .
docker run -p 8000:8000 banking-backend
```
