#!/usr/bin/python
#run.py
import sys
sys.path.append("/usr/lib/python2.7/site-packages")
from flask import Flask, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import json, threading, time, interface, os.path, signal

print(sys.path)

app = Flask(__name__, static_url_path='')
CORS(app)

class Server():
	def __init__(self):
		self.interface = interface.Main("/home/pi/SawyerSensopart/param.json")

server = Server()

class Multirun():
	def __init__(self, runnum):
		self.runnum = runnum
		self.t = threading.Thread(target = self.run)
		self.t.start()

	def run(self):
		if(self.runnum == 0):
			self.flask_run()
		else : 
			self.socket_run()

	def flask_run(self):
		app.run(host='0.0.0.0')

	def socket_run(self):
		server.interface.camera.socket_run()
		
@app.route('/')  #load home page
def render_static():
    return render_template('config.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js',path)

@app.route("/GET/IPSawyer", methods=["GET"])
def getIPSawyer():
	tmp = server.interface.sawyer.config["IP"]
	return json.dumps(tmp),200, {'Content-Type':'application/json'}

@app.route("/GET/portSawyer", methods=["GET"])
def getPortSawyer():
	tmp = server.interface.sawyer.config["port"]
	return json.dumps(tmp),200, {'Content-Type':'application/json'}

@app.route("/GET/IPCamera", methods=["GET"])
def getIPserverCamera():
	tmp = server.interface.camera.config["IP"]
	return json.dumps(tmp),200, {'Content-Type':'application/json'}

@app.route("/GET/portCamera", methods=["GET"])
def getPortCamera():
	tmp = server.interface.camera.config["port"]
	return json.dumps(tmp),200, {'Content-Type':'application/json'}

@app.route("/GET/connexionSawyer", methods=["GET"])#get connection status from Sawyer
def getConnexionSawyer():
	tmp = server.interface.sawyer.connec_test
	return json.dumps(tmp),200, {'Content-Type':'application/json'}

@app.route("/GET/connexionCamera", methods=["GET"]) #get connection status from Camera
def getConnexionCamera():
	tmp = server.interface.camera.connec_test
	return json.dumps(tmp),200, {'Content-Type':'application/json'}
#------------------------------------------------------------------------------------------
@app.route("/POST/IPSawyer",methods=["POST"])
def postIPSawyer():
 	tmp = request.get_data()
 	tmp = json.loads(tmp)
 	server.interface.sawyer.set_ip(tmp)
 	return json.dumps(tmp),200,{'Content-Type':'application/json'}


@app.route("/POST/IPCamera",methods=["POST"])
def postIPCamera():
 	tmp = request.get_data()
 	tmp = json.loads(tmp)
 	server.interface.camera.set_ip(tmp)
 	return json.dumps(tmp),200,{'Content-Type':'application/json'}

@app.route("/POST/portSawyer",methods=["POST"])
def postPortSawyer():
 	tmp = request.get_data()
 	tmp = json.loads(tmp)
 	server.interface.sawyer.set_port(tmp)
 	return json.dumps(tmp),200,{'Content-Type':'application/json'}

@app.route("/POST/portCamera",methods=["POST"])
def postPortCamera():
	tmp = request.get_data()
	tmp = json.loads(tmp)
	server.interface.camera.set_port(tmp)
	return json.dumps(tmp),200,{'Content-Type':'application/json'}


@app.route("/tryConnectSawyer") #get connection status from Camera
def tryConnectSawyer():
	server.interface.sawyer.connection();
	return 200,{'Content-Type':'application/json'}

@app.route("/tryConnectCamera") #get connection status from Camera
def tryConnectCamera():
	server.interface.camera.connection();
	return 200,{'Content-Type':'application/json'}

if __name__ == "__main__":
	#executing flask  and socket in threading
	for i in range(2):
		a = Multirun(i)
	try:
		while True:
			time.sleep(10)
	except KeyboardInterrupt:
		os.kill(os.getpid(), signal.SIGTERM )

