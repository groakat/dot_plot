import os, io
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug import secure_filename

import sys, os, glob
sys.path.append('/home/peter/code/plotting/')

import numpy as np
import matplotlib as mpl
import pylab as plt
import plotting.python.dotPlot as dp


UPLOAD_FOLDER = '/home/peter/code/plotting/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return plot_file(filename=filename)
            #~ return redirect(url_for('uploaded_file',
                                    #~ filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
        
@app.route('/uploads/<filename>')
def show_file(filename):
    print "show file"
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
#~ @app.route('/uploads/<filename>')
def plot_file(filename):
    
    print "plotting"
    
    with io.open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as f:
        header = f.readline().strip('\n').split('\t')
        a = np.genfromtxt(f, delimiter='\t', missing_values='')
                    
    d =  zip(*a)
    x = []
    fig = plt.figure(figsize=(len(d) * 2 + 2, 12))    
    for i in range(len(d)):
        hist = np.histogram(d[i], bins=4, range=(1,6))
        dp.plotDotPlot(hist, space=0.15, os=i*2, width=5, facecolors='black',marker='o', s=10)
        x += [[i*2, header[i]]]
        
    plt.axes().set_aspect('equal')
    plt.axes().set_autoscale_on(False)
    plt.axes().set_ybound(0,6)
    plt.axes().set_xbound(-0.9, i* 2 + 0.9)
    
    plt.xticks(zip(*x)[0], zip(*x)[1] )
    plt.yticks(range(1,6))
    
    fn = filename.split('.csv')[0] + '.png'
    fig.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 
                fn),dpi=300, format='png')
                
    return redirect(url_for('show_file', filename=fn))
                              
    
                               
if __name__ == "__main__":
    app.run()#debug=True)

