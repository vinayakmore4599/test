# AI Q&A Assistant - Setup Guide

This application allows users to ask questions through a React-based UI, get answers from Perplexity AI, and download the Q&A as PDF.

## Features

✅ **React UI** - Modern, responsive interface for asking questions  
✅ **Perplexity Integration** - Real-time answers from Perplexity AI API  
✅ **PDF Export** - Download questions and answers as formatted PDFs  
✅ **Message History** - View all Q&A conversations in the chat interface  
✅ **Error Handling** - Graceful error messages and loading states  

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Perplexity AI API key

## Installation & Setup

### 1. Get Perplexity API Key

1. Visit [Perplexity AI API](https://www.perplexity.ai/settings/api)
2. Sign up or log in to your account
3. Create an API key
4. Copy the API key

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Perplexity API key
# Open .env in your editor and replace 'your-api-key-here' with your actual key
```

**File: `.env`**
```
PERPLEXITY_API_KEY=your-actual-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Run the Application

```bash
# Start the Flask server
python app.py
```

The application will be available at: **http://localhost:5000**

## Usage

1. **Open the Web Interface**: Navigate to http://localhost:5000 in your browser
2. **Ask a Question**: Type your question in the text area and press "Send" or Ctrl+Enter
3. **View Answer**: Wait for Perplexity AI to respond with an answer
4. **Download PDF**: Click the "📥 Download PDF" button below each answer to save it as a PDF file

## Application Architecture

### Backend (Flask)

- **`/`** - Serves the React UI
- **`/api/ask`** - Receives questions, calls Perplexity API, returns answers
- **`/api/download-pdf`** - Generates and downloads PDF with Q&A

### Frontend (React)

- **React 18** - For building interactive UI
- **Babel** - For JSX compilation
- **CDN** - React, ReactDOM, and Babel loaded via CDN for quick setup

## Dependencies

- **Flask** - Web framework for Python
- **Flask-CORS** - Handles CORS for API requests
- **requests** - HTTP library for API calls
- **reportlab** - PDF generation
- **python-dotenv** - Environment variable management

## Troubleshooting

### "Invalid API Key" Error
- Verify your Perplexity API key in `.env`
- Ensure the API key is valid and active
- Check that PERPLEXITY_API_KEY is set correctly

### "Connection Timeout" Error
- Check your internet connection
- Perplexity API might be temporarily unavailable
- Try again after a few moments

### CORS Errors
- Flask-CORS is enabled to handle cross-origin requests
- If issues persist, check that Flask is running

### PDF Download Not Working
- Ensure reportlab is properly installed: `pip install reportlab`
- Check that your browser allows downloads
- Try a different browser if issues persist

## Development

### Project Structure
```
/test
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Example environment file
├── SETUP.md              # This file
├── README.md             # Original README
├── README_APP.md         # App-specific README
└── templates/
    └── index.html        # React frontend application
```

### Making Changes

1. **Backend Changes**: Restart Flask server (`python app.py`)
2. **Frontend Changes**: Refresh browser (no build step needed with CDN)

## API Reference

### POST /api/ask
**Request:**
```json
{
  "question": "What is machine learning?"
}
```

**Response:**
```json
{
  "question": "What is machine learning?",
  "answer": "Machine learning is...",
  "timestamp": "2024-01-10T12:34:56.789Z"
}
```

### POST /api/download-pdf
**Request:**
```json
{
  "question": "What is machine learning?",
  "answer": "Machine learning is..."
}
```

**Response:** Binary PDF file

## Perplexity API Models

Current model: `pplx-7b-online`

Other available models:
- `pplx-7b-chat` - Lightweight chat model
- `pplx-70b-online` - More powerful online model
- `pplx-70b-chat` - More powerful chat model

To change the model, edit the `payload['model']` in `app.py` line ~52.

## Security Notes

⚠️ **Important:**
- Never commit `.env` with real API keys to version control
- `.env` is in `.gitignore` by default
- Keep your Perplexity API key confidential
- Rotate API keys periodically for production use

## Support

For issues with:
- **Perplexity API**: Visit https://www.perplexity.ai/help
- **Flask**: https://flask.palletsprojects.com/
- **React**: https://react.dev/

## License

This project is open source and available under the MIT License.
