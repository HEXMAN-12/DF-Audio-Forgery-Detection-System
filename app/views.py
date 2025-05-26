import os
import uuid
from flask import (
    Blueprint, flash, redirect, render_template, 
    request, url_for, current_app, send_from_directory
)
from werkzeug.utils import secure_filename
from .forms import UploadForm
from .audio_analysis import analyze_audio_file

bp = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=('GET', 'POST'))
def index():
    form = UploadForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Generate a unique filename to prevent overwriting
            original_filename = secure_filename(file.filename)
            filename = f"{uuid.uuid4()}_{original_filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Analyze the audio file
            result, plots = analyze_audio_file(filepath)
            
            return render_template('results.html', 
                                  result=result, 
                                  plots=plots, 
                                  filename=original_filename)
        else:
            flash('File type not allowed. Please upload a WAV file.')
            
    return render_template('index.html', form=form)

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')
