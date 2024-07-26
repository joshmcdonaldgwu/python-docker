#starting the app from within the folder just requires flask --app hello run
#it will be on http://127.0.0.1:5000 by default
'''
General requirements
'''
import os
import csv
import random
import shutil
from time import sleep

'''
Flask app requirements
'''
from flask import Flask, render_template, request, flash, url_for, redirect, abort
from distutils.log import debug 
from fileinput import filename 
from threading import Timer
from werkzeug.utils import secure_filename

'''
QR code and image libraries
'''
#segno may need to be installed separately: https://pypi.org/project/segno/
import segno
from PIL import Image

'''
web browser and url libraries
'''
#urllib request *might* conflict with flask request?
#from urllib import request
#webdriver also requires that you have one or another browser driver installed. 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.tsv', '.png', '.gif']

@app.route('/')
def index():
    return render_template('index.html')
'''
demonstrating how to use a text form, can we also use a file-picker? 
'''
#there are probably better ways to handle this, but . . . does it work?
#https://www.geeksforgeeks.org/how-to-upload-file-in-python-flask/
#also: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
@app.route('/upload/')
def upload():   
    return render_template('upload.html')

@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        uploaded_file = request.files['file'] 
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            file_path = os.path.join(app.config['UPLOAD_PATH'], filename)    
            uploaded_file.save(file_path)
            assert 'tsv' in file_path, "This has to be a TSV file as written."
            with open(file_path, newline='') as f:
                reader = csv.reader(f, delimiter="\t")
                data = list(reader)
                print(data[1])
            #uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))    
        return render_template("Acknowledgement.html", name = os.path.join(app.config['UPLOAD_PATH'], filename))   

#open browser automatically - commenting this out while dockerizing.
'''
def open_browser():
    browser = webdriver.Firefox()
    browser.get('http://127.0.0.1:5000')

if __name__ == "__main__":
      Timer(1, open_browser).start()
      app.run(port=5000, debug=True)
'''

      
'''
https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
seems to cover the file part, but do we actually need to pull the file into the app? 
what are the pros/cons for doing this? 
    * the text files are small, image files would still be better stored on the user side though. 
it seems like the file browser could still be tkinter-based. 
https://stackoverflow.com/questions/23775211/flask-desktop-application-file-chooser

'''

'''
@app.route('api/filedialog', methods = ['POST'])
def open_filedialog():
    """open file dialog to get a file name"""

    print(request.json)
    filename = 'not found'
    root = tk.Tk()
    
    filename = askopenfilename()
    
    root.withdraw()
    if filename == 'not found':
        root.mainloop()
    else:
        root.destroy()
    

    #if filename selected new file name
    
    if filename:
        return jsonify({'file' : filename}), 200
    #else old file name
    else:
        return jsonify(request.json), 200
'''