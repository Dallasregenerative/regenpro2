# RegenMed AI Pro - Setup Instructions

## Environment Setup

### Backend Setup
1. Copy the environment template:
   ```bash
   cp backend/.env.example backend/.env
   ```

2. Add your OpenAI API key to `backend/.env`:
   ```
   OPENAI_API_KEY="your-actual-openai-api-key-here"
   ```

### Frontend Setup
The frontend `.env` file contains deployment-specific URLs and should be configured for your environment.

## Security Notes
- Never commit `.env` files to version control
- Keep API keys secure and rotate them regularly
- Use environment-specific configurations for different deployments

## API Keys Required
- OpenAI API Key (for AI analysis and protocol generation)

## Getting Started
1. Install dependencies: `pip install -r backend/requirements.txt`
2. Start services: `sudo supervisorctl start all`
3. Access the platform at `http://localhost:3000`