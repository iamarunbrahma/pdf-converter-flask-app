#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request
from flask import send_file, redirect, url_for, after_this_request
from werkzeug.utils import secure_filename
import pathlib, os, io, shutil
from pdf_converter import convert_docx, convert_pdf


app = Flask(__name__)

allowed_extensions = set(['.docx', '.pdf'])

parent_dir = pathlib.Path(__file__).parent.absolute()
app.config['TEMP_FOLDER'] = pathlib.Path(parent_dir,'static','files','temp')

shutil.rmtree(app.config['TEMP_FOLDER'], ignore_errors = True)


def allowed_file(filename):
    return '.' in filename and \
        pathlib.Path(filename).suffix in allowed_extensions


@app.route('/', methods = ['GET'])
def home():
    pathlib.Path(app.config['TEMP_FOLDER']).mkdir(parents=True, exist_ok=True)
    return render_template('index.html')


# @app.route('/home', methods=['GET', 'POST'])
@app.route('/upload',methods = ['GET' , 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if pathlib.Path(filename).suffix == '.pdf':
                app.config['MIME_TYPE'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                upload_file = pathlib.Path(app.config['TEMP_FOLDER'], filename)
                file.save(upload_file)
                output_file = convert_docx(upload_file, app.config['TEMP_FOLDER'])

                if os.path.exists(upload_file):
                    os.remove(upload_file)

                return redirect(url_for('download_file', path = output_file))


            elif pathlib.Path(filename).suffix == '.docx':
                app.config['MIME_TYPE'] = 'application/pdf'
                upload_file = os.path.join(app.config['TEMP_FOLDER'], filename)
                file.save(upload_file)
                output_file = convert_pdf(upload_file, app.config['TEMP_FOLDER'])

                if os.path.exists(upload_file):
                    os.remove(upload_file)

                return redirect(url_for('download_file', path = output_file))

            else:
                return render_template("index.html", msg="Error in processing your file. Pls try again")
        else:
            return render_template("index.html", msg="Oops Sorry! Pls upload either .docx or .pdf files")

    return render_template('index.html')



@app.route('/download/<path>')
def download_file(path):    
    download_path = pathlib.Path(app.config['TEMP_FOLDER'], path)

    if os.path.exists(download_path):
        return_data = io.BytesIO()

        with open(download_path, 'rb') as f:
            return_data.write(f.read())

        return_data.seek(0)
        os.remove(download_path)
        # return send_file(path, as_attachment = True)

        return send_file(return_data, mimetype = app.config['MIME_TYPE'],
                     attachment_filename = path, as_attachment = True)

    else:
        return render_template("index.html", msg="404 Bad Request. Kindly try again.")


if __name__ == '__main__':
    app.run()

