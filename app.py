from flask import Flask, render_template, request, send_from_directory
import qrcode
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qrcodes/'

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get form data
        data = request.form['data']
        fill_color = request.form.get('fill_color', 'black')
        back_color = request.form.get('back_color', 'white')

        # Generate unique filename
        filename = f"qr_{uuid.uuid4().hex}.png"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(save_path)

        return render_template('result.html', qr_image=filename)

    return render_template('index.html')


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)