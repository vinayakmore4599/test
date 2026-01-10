from flask import Flask, render_template, request, send_file
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '')
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        p.setFont('Helvetica', 12)
        margin_x = 72
        y = height - 72
        line_height = 14
        for raw_line in text.splitlines() or ['']:
            line = raw_line
            while len(line) > 0:
                chunk = line[:90]
                p.drawString(margin_x, y, chunk)
                line = line[90:]
                y -= line_height
                if y < 72:
                    p.showPage()
                    p.setFont('Helvetica', 12)
                    y = height - 72
        p.showPage()
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='output.pdf', mimetype='application/pdf')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
