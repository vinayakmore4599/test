from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration - All loaded from .env file
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
PERPLEXITY_API_URL = 'https://api.perplexity.ai/chat/completions'
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
FLASK_ENV = os.getenv('FLASK_ENV', 'development')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Send question to Perplexity.ai and return answer"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Call Perplexity API
        headers = {
            'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'sonar',
            'messages': [
                {'role': 'user', 'content': question}
            ],
            'temperature': 0.7,
            'max_tokens': 1024
        }
        
        response = requests.post(
            PERPLEXITY_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            return jsonify({
                'error': f'Perplexity API error: {response.status_code}',
                'details': response.text
            }), response.status_code
        
        result = response.json()
        answer = result['choices'][0]['message']['content']
        
        return jsonify({
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout - Perplexity API took too long to respond'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/download-pdf', methods=['POST'])
def download_pdf():
    """Generate and download PDF with question and answer"""
    try:
        data = request.json
        question = data.get('question', '')
        answer = data.get('answer', '')
        
        if not question or not answer:
            return jsonify({'error': 'Question and answer are required'}), 400
        
        # Generate PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Set up fonts
        p.setFont('Helvetica-Bold', 14)
        margin_x = 50
        y = height - 50
        line_height = 14
        
        # Add question
        p.drawString(margin_x, y, 'Question:')
        y -= line_height
        p.setFont('Helvetica', 11)
        
        # Wrap question text
        for raw_line in question.splitlines() or ['']:
            line = raw_line
            while len(line) > 0:
                chunk = line[:85]
                p.drawString(margin_x + 20, y, chunk)
                line = line[85:]
                y -= line_height
                if y < 50:
                    p.showPage()
                    p.setFont('Helvetica', 11)
                    y = height - 50
        
        # Add spacing
        y -= line_height
        
        # Add answer heading
        p.setFont('Helvetica-Bold', 14)
        p.drawString(margin_x, y, 'Answer:')
        y -= line_height
        p.setFont('Helvetica', 11)
        
        # Wrap answer text
        for raw_line in answer.splitlines() or ['']:
            line = raw_line
            while len(line) > 0:
                chunk = line[:85]
                p.drawString(margin_x + 20, y, chunk)
                line = line[85:]
                y -= line_height
                if y < 50:
                    p.showPage()
                    p.setFont('Helvetica', 11)
                    y = height - 50
        
        # Add metadata
        p.setFont('Helvetica', 8)
        p.drawString(margin_x, 30, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        p.showPage()
        p.save()
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'qa_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'PDF generation error: {str(e)}'}), 500


if __name__ == '__main__':
    import sys
    # Get port from command line argument or environment variable or default
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = int(os.getenv('PORT', 8000))
    
    print(f"\n{'='*60}")
    print(f"🚀 Flask server starting on http://localhost:{port}")
    print(f"Environment: {FLASK_ENV}")
    print(f"Debug Mode: {FLASK_DEBUG}")
    print(f"{'='*60}\n")
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=port)
