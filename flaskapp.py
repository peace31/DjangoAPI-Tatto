import flask
from flask import Flask,url_for
from functools import wraps
from flask import *
from flask import send_from_directory
import base64
import os
import cv2
import pix2pix as pp
import numpy as np
import time
import shutil

UPLOAD_FOLDER ='/home/ubuntu/flaskapp/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def get_combine():
    output_dir='/home/ubuntu/flaskapp/uploads/c'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    input_dir='/home/ubuntu/flaskapp/uploads/b'
    b_dir='/home/ubuntu/flaskapp/uploads/a'
    H=256
    skipped = 0
    for f in os.listdir(input_dir):
        src_path=os.path.join(input_dir,f)
        img1=cv2.imread(src_path)
        flag=0
        sibling_path = os.path.join(b_dir, f)
        if os.path.exists(sibling_path):
            img2 = cv2.imread(sibling_path)
            flag=1
        if(flag==0):
            continue
        img1=cv2.resize(img1, (H,H)) 
        img2=cv2.resize(img2, (H,H)) 
        vis = np.zeros((H, 2*H,3), np.uint8)
        vis[:H, :H] = img1
        vis[:H, H:2*H] = img2
        ff=f.split('.')
        dst_path = os.path.join(output_dir, ff[0] + ".png")
        cv2.imwrite(dst_path,vis)
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET', 'POST'])
def imageupload():
	if request.method == 'POST':
		# return json.dumps({'status': app.config['UPLOAD_FOLDER']})
		files=request.files

		# check if the post request has the file part
		if files is None or len(files)==0:
			flash('No file part')
			return json.dumps({'status': 'No file part'})
		shutil.rmtree(app.config['UPLOAD_FOLDER']+'/a')
		os.makedirs(app.config['UPLOAD_FOLDER']+'/a')
		for i in range(len(files)):
			file=files['file'+str(i)]
			# if user does not select file, browser also
			# submit a empty part without filename
			if file.filename == '':
				continue
			
			if file and allowed_file(file.filename):
				filename = file.filename
				# return json.dumps({'status':'ok', 'filename': filename})
				path=os.path.join(app.config['UPLOAD_FOLDER']+"/a", filename)
				# return json.dumps({'status':'ok', 'filename': os.path.dirname(np.__file__)})
				file.save(path)
		return json.dumps({'status':'ok', 'filepath': app.config['UPLOAD_FOLDER']+'/a'})
	return json.dumps({'status': "Failed"})
@app.route('/upload1', methods=['GET', 'POST'])
def imageupload1():
	if request.method == 'POST':
		# return json.dumps({'status': app.config['UPLOAD_FOLDER']})
		files=request.files

		# check if the post request has the file part
		if files is None or len(files)==0:
			flash('No file part')
			return json.dumps({'status': 'No file part'})
		shutil.rmtree(app.config['UPLOAD_FOLDER']+'/b')
		os.makedirs(app.config['UPLOAD_FOLDER']+'/b')
		for i in range(len(files)):
			file=files['file'+str(i)]
			# if user does not select file, browser also
			# submit a empty part without filename
			if file.filename == '':
				continue
			
			if file and allowed_file(file.filename):
				filename = file.filename
				# return json.dumps({'status':'ok', 'filename': filename})
				path=os.path.join(app.config['UPLOAD_FOLDER']+"/b", filename)
				# return json.dumps({'status':'ok', 'filename': os.path.dirname(np.__file__)})
				file.save(path)
		shutil.rmtree(app.config['UPLOAD_FOLDER']+'/c')
		os.makedirs(app.config['UPLOAD_FOLDER']+'/c')
		get_combine()
		return json.dumps({'status':'ok', 'filepath': app.config['UPLOAD_FOLDER']+'/b'})
	return json.dumps({'status': "Failed"})
@app.route('/process', methods=['POST'])
def process():
	if request.method == 'POST':
		input_dir='/home/ubuntu/flaskapp/uploads/c'
		output_dir='/home/ubuntu/flaskapp/c_train'
		shutil.rmtree(output_dir)
		os.makedirs(output_dir)
		r=pp.main(input_dir,output_dir)
		return json.dumps({'status':r})
	else:
		return None
@app.route('/')
def hello_world():
  return 'Hello from Flask!'

@app.route('/main')
def mainpage():
	error = None
	return render_template('home.html', error=error)
@app.route('/test_page')
def testpage():
	error = None
	return render_template('test_page.html', error=error)

@app.route('/upload_test', methods=['GET', 'POST'])
def upload_test():
	if request.method=='POST':
		if 'file' not in request.files:
			return json.dumps({'status': 'No file part'})
		file =request.files['file']
		if file.filename =='':
			return json.dumps({'status': 'No Selected file'})
		if file and allowed_file(file.filename):
			path='/home/ubuntu/flaskapp/c_test/test.png'
			file.save(path)
			return json.dumps({'status': 'ok'})
	return json.dumps({'status': 'unsuccess'})
@app.route('/test_process', methods=['GET', 'POST'])
def test_process():
	if request.method=='POST':
		input_path='/home/ubuntu/flaskapp/c_test/test.png'
		output_path='/home/ubuntu/flaskapp/input_image/test.png'
		img=cv2.imread(input_path)
		height, width = img.shape[:2]
		H=256
		save_img=cv2.resize(img, (H,H)) 
		vis = np.zeros((H, 2*H,3), np.uint8)
		vis[:H, :H] = save_img
		vis[:H, H:2*H] = save_img
		cv2.imwrite(output_path,vis)
		input_dir='/home/ubuntu/flaskapp/input_image'
		output_dir='/home/ubuntu/flaskapp/d_test'
		checkpoint_dir='/home/ubuntu/flaskapp/c_train'
		r=pp.main(input_dir,output_dir,checkpoint_dir,200,'test')
		outputpath='/home/ubuntu/flaskapp/d_test/images/test-outputs.png'
		img=cv2.imread(outputpath)
		img1=cv2.resize(img,(width,height))
		cv2.imwrite('/home/ubuntu/flaskapp/static/output.png',img1)
		timestamp = str(time.time()).replace('.','_')
		return json.dumps({'filename':'static/output.png?updated=' + timestamp,'src':url_for('static', filename='output.png')})
	return json.dumps({'status': 'unsuccess'})
if __name__ == '__main__':
  app.run()