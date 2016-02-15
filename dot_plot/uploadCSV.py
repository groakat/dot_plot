import os, io
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug import secure_filename

import sys, os, glob
sys.path.append('/home/peter/code/plotting/')

import numpy as np
import matplotlib as mpl
import pylab as plt
import dotPlot as dp


UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print "upload"
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return plot_file(filename=filename)
            # return redirect(url_for('uploaded_file',
            #                         ~ filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
         <input type=checkbox name=do_vector value="do_vector"> generate vector graphic
    </form>
    '''
        
@app.route('/uploads/<filename>')
def show_file(filename):
    print "show file"
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/uploads/<filename>')
def plot_file(filename):
    
    print "plotting"
        
    df = dp.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    fig = dp.plot_matplot_lib(df)

    if request.form.getlist("do_vector"):
        extension = 'svg'
    else:
        extension = 'png'
    
    fn = filename.split('.csv')[0] + '.' + extension
    fig.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 
                fn),dpi=300, format=extension)
                
    return redirect(url_for('show_file', filename=fn))
                              
    
                               
if __name__ == "__main__":
    mpl.rcParams.update({'font.size': 28, 'svg.fonttype': 'none'})
    app.run(debug=True)

