# Troubleshooting Guide - Perplexity API Configuration

## Recent Changes Made

✅ **Updated API Endpoint**: Changed from `https://api.perplexity.ai/openai/chat/completions` to `https://api.perplexity.ai/chat/completions`

✅ **Updated Model**: Changed from deprecated `pplx-7b-online` to `sonar` (current valid model)

✅ **Centralized Configuration**: All settings (API key, port, environment) are now in `.env` file

✅ **Smart Scripts**: `start.sh` and `stop.sh` now read configuration from `.env`

## Common Issues & Solutions

### Issue 1: 404 Error from Perplexity API
**Cause**: Incorrect API endpoint URL

**Solution**: The endpoint has been fixed to use `https://api.perplexity.ai/chat/completions`

**Verification**: Test with curl:
```bash
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "pplx-7b-online",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Issue 2: Unauthorized/Invalid API Key (401)
**Cause**: API key is invalid or expired

**Steps**:
1. Get a fresh API key from https://www.perplexity.ai/settings/api
2. Update your `.env` file:
   ```
   PERPLEXITY_API_KEY=your-new-api-key
   ```
3. Restart the application: `./start.sh`

### Issue 3: Port Already in Use
**Solution**: Use the provided scripts:
```bash
# Stop the application
./stop.sh

# Start on a different port
PORT=9000 python3 app.py
```

## Configuration File (.env)

Your `.env` file should look like:
```
# Perplexity API Configuration
PERPLEXITY_API_KEY=your-api-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Server Port Configuration
PORT=8000
```

## Available Models

You can change the model in `app.py` (line ~50):
- `sonar` (current) - Lightweight search model with web grounding
- `sonar-pro` - Advanced search with complex queries
- `sonar-reasoning-pro` - Advanced reasoning with Chain of Thought
- `sonar-deep-research` - Expert-level research model

For more details, visit: https://docs.perplexity.ai/getting-started/models

## Testing Steps

1. **Start the server**:
   ```bash
   ./start.sh
   ```
   
   Should output:
   ```
   ============================================================
   🚀 Flask server starting on http://localhost:8000
   Environment: development
   Debug Mode: True
   ============================================================
   ```

2. **Open browser**: Go to `http://localhost:8000`

3. **Ask a test question**: "What is Python?"

4. **Check console output** for any errors

5. **Stop the server**:
   ```bash
   ./stop.sh
   ```

## File Structure

```
/test
├── app.py                    # Flask backend (updated)
├── .env                      # Configuration (sensitive)
├── .env.example              # Configuration template
├── start.sh                  # Start server script (updated)
├── stop.sh                   # Stop server script (updated)
├── kill_ports.sh             # Kill processes on specific ports
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # React UI
├── SETUP.md                 # Setup instructions
└── README.md                # Original README
```

## Next Steps

1. Verify your API key is valid
2. Run `./start.sh` to start the server
3. Test in browser at `http://localhost:8000`
4. If still getting errors, check the console output for detailed error messages

## Need Help?

- **Perplexity API Docs**: https://docs.perplexity.ai/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Check the error message**: The detailed error from Perplexity API will help identify the issue
