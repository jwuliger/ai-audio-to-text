from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
import uuid

from audio_to_text import convert_audio_to_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULT_FOLDER'] = 'results/'
app.config['ALLOWED_EXTENSIONS'] = {'wav'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['RESULT_FOLDER']):
    os.makedirs(app.config['RESULT_FOLDER'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        return render_template('index.html')
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if not file or not allowed_file(file.filename):
        return 'Invalid file format', 400
    # filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{file_id}.wav'))
    transcript = convert_audio_to_text(
        os.path.join(app.config['UPLOAD_FOLDER'], f'{file_id}.wav')
    )
    with open(os.path.join(app.config['RESULT_FOLDER'], f'{file_id}.txt'), 'w') as result_file:
        result_file.write(transcript)
    return send_from_directory(
        app.config['RESULT_FOLDER'], f'{file_id}.txt', as_attachment=True
    )


if __name__ == '__main__':
    app.run(debug=True)
