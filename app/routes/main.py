from flask import Blueprint, render_template, request, redirect, session
from app.auth.email import send_verification_email
from app.auth.validator import validate_email_domain, verify_code
from app.upload.uploader import handle_upload

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
    blobs = bucket.list_blobs(prefix='public/')
    projects = set()
    for blob in blobs:
        parts = blob.name.split('/')
        if len(parts) > 1 and parts[1]:
            projects.add(parts[1])
    return render_template('files.html', projects=sorted(projects))

@main_bp.route('/project/<project_name>')
@login_required
def view_project(project_name):
    bucket_name = os.environ.get('GCS_BUCKET_NAME')
    bucket = gcs_client.bucket(bucket_name)
    prefix = f'public/{project_name}/'
    blobs = bucket.list_blobs(prefix=prefix)

    readme_content = ''
    file_list = []

    for blob in blobs:
        rel_path = blob.name[len(prefix):]
        if rel_path == 'README.md':
            readme_content = blob.download_as_text()
        elif rel_path:
            file_list.append(rel_path)

    return render_template('project.html',
                           project_name=project_name,
                           readme_content=readme_content,
                           files=sorted(file_list))