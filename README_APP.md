# Simple Text-to-PDF App

This small Flask app accepts user text and returns a downloadable PDF containing that text.

Run locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 in your browser, paste text and click "Generate PDF".
