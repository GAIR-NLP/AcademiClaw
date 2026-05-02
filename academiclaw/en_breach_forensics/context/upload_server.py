import os
from flask import Flask, request, abort
import config

app = Flask(__name__)
app.config.from_object(config.Config)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'png'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files: return 'No file', 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return 'Success', 201
    return 'Invalid', 403
