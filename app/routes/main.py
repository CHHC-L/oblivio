from flask import Blueprint, render_template, request, redirect, session
from app.auth.email import send_verification_email
from app.auth.validator import validate_email_domain, verify_code
from app.upload.uploader import handle_upload
from app.utils.decorator import login_required
from app import gcs_client
import os, re
from collections import defaultdict

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        if validate_email_domain(email):
            send_verification_email(email)
            return redirect('/verify')
        return "Unauthorized domain", 403
    return render_template('register.html')

@main_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        email = request.form['email']
        code = request.form['code']
        if verify_code(email, code):
            session['user'] = email
            return redirect('/files')
        return "Verification failed", 401
    return render_template('verify.html')

@main_bp.route('/files')
@login_required
def list_projects():
    bucket_name = os.environ.get('GCS_BUCKET_NAME')
    bucket = gcs_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    projects = set()
    for blob in blobs:
        print(f"[GCS] list_projects() -> blob: {blob.name}")
        if '/' in blob.name:
            project_name = blob.name.split('/', 1)[0]
            if project_name:
                projects.add(project_name)
    return render_template('files.html', projects=sorted(projects))

@main_bp.route('/project/<project_name>')
@login_required
def view_project(project_name):
    if not re.match(r'^[a-zA-Z0-9_.-]+$', project_name):
        return "Invalid project name", 400
    
    bucket_name = os.environ.get('GCS_BUCKET_NAME')
    bucket = gcs_client.bucket(bucket_name)
    prefix = f'{project_name}/'
    blobs = bucket.list_blobs(prefix=prefix)

    readme_content = ''
    file_list = []

    for blob in blobs:
        rel_path = blob.name[len(prefix):]
        lower_path = rel_path.lower()
        if lower_path == 'readme' or lower_path.startswith('readme.'):
            readme_content = blob.download_as_text()
        if rel_path:
            file_list.append(rel_path)
            print(f"[GCS] view_project({project_name}) -> rel_path: {blob.name}")

    return render_template('project.html',
                           project_name=project_name,
                           readme_content=readme_content,
                           files=sorted(file_list))

@main_bp.route('/project/<project_name>/file/<filepath>')
@login_required
def view_file(project_name, filepath):
    if not re.match(r'^[a-zA-Z0-9_.-]+$', project_name):
        return "Invalid project name", 400

    bucket_name = os.environ.get('GCS_BUCKET_NAME')
    bucket = gcs_client.bucket(bucket_name)
    blob_path = f'public/{project_name}/{filepath}'
    blob = bucket.blob(blob_path)
    if not blob.exists():
        return "File not found", 404
    content = blob.download_as_text()
    return render_template('file_view.html', project_name=project_name, filepath=filepath, content=content)
