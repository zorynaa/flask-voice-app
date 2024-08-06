import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PASSWORD'] = 'yourpassword'  # Set your password here

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app.config['PASSWORD']:
            file = request.files['file']
            if file and file.filename.endswith('.wav'):  # Check for voice message file type
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'voicemessage.wav'))
                return redirect(url_for('uploaded_file'))
            else:
                return "Invalid file format. Please upload a .wav file."
        else:
            return "Invalid password."
    return render_template('index.html')

@app.route('/uploads/voicemessage.wav')
def uploaded_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'voicemessage.wav')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
