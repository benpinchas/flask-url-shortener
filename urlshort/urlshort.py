from flask import (render_template,request, redirect, url_for, flash, abort, session, jsonify, Blueprint)
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)

URL_REGISTRY = 'urls.json'

@bp.route('/')
def home():
   return render_template('home.html', name='Ben', codes=session.keys())

@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists(URL_REGISTRY):
            with open(URL_REGISTRY) as urls_file:
                urls = json.load(urls_file)

        code = request.form['code']

        if code in urls:
            flash('Hey this code has already been taken. please select another code.')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[code] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = code + secure_filename(f.filename)
            f.save('/Users/benpinchas/dev/flask_essentials_linkedin_Project/url-shortener/urlshort/static/users_files/' + full_name)
            urls[code] = {'file': full_name}

        with open(URL_REGISTRY, 'w') as url_file:
            json.dump(urls, url_file)
            session[code] = True # could be timestamp also

        return render_template('your_url.html', code=request.form['code']) #code=request.args['code'] # GET request
    else:
        url = url_for('urlshort.home')
        return redirect(url)

@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists(URL_REGISTRY):
        with open(URL_REGISTRY, 'r') as urls_file:
            urls = json.load(urls_file)
            if code in urls:
                entity = urls[code]
                if 'url' in entity:
                    url = entity['url']
                elif 'file' in entity:
                    filename = entity['file']
                    url = url_for('static', filename=f'users_files/{filename}')
                
                return redirect(url)

    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return  jsonify(list(session.keys()))









