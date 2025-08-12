# RegenMed AI Pro - Setup Instructions

## Environment Variables & Security

⚠️ **IMPORTANT SECURITY NOTE**: Never commit API keys or sensitive credentials to version control.

### Required Environment Variables

1. **Backend Environment Setup**:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Configure your API keys in `backend/.env`**:
   ```
   MONGO_URL="mongodb://localhost:27017"
   DB_NAME="test_database"
   OPENAI_API_KEY="your-actual-openai-api-key-here"
   ```

3. **Frontend Environment Setup**:
   ```bash
   cd frontend
   cp .env.example .env
   ```

### Getting Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in to your account
3. Create a new API key
4. Copy the key (starts with `sk-proj-...`)
5. Replace `your-actual-openai-api-key-here` in `backend/.env`

### Security Features

- ✅ `.env` files are automatically ignored by git
- ✅ `.env.example` files show structure without exposing secrets
- ✅ GitHub security protection will block accidental commits
- ✅ All sensitive data stays local to your machine

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd backend && pip install -r requirements.txt
   cd ../frontend && yarn install
   ```

2. **Start Services**:
   ```bash
   sudo supervisorctl restart all
   ```

3. **Access the Platform**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8001`

## Troubleshooting

### GitHub Push Protection
If you see "Security Protection Activated", it means sensitive data was detected:
1. Check that `.env` files are not staged: `git status`
2. Ensure `.gitignore` includes `.env` patterns
3. Use `.env.example` templates for structure
4. Keep actual credentials in local `.env` files only

### API Key Issues
- Ensure OpenAI API key is properly formatted
- Check that you have sufficient API credits
- Verify the key is placed in `backend/.env`, not `frontend/.env`

## Production Deployment

When deploying to production:
1. Use environment variables instead of `.env` files
2. Set `OPENAI_API_KEY` as a secure environment variable
3. Configure `MONGO_URL` for your production database
4. Never expose API keys in client-side code