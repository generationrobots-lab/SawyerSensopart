#Scipt to convert data from the camera by 1000
#and send it to sawyer by TCP/IP protocol.

#!/usr/bin/env python
import socket
import time 
import json
#paramater file which is possible to change via web page

class Interface():
	def __init__(self,main, config):
		self.config = config #load IP and port dictionnary 
		self.connec_test = 0 
		self.main = main
		
	def set_ip(self, newIP): #function to change IP of sawyer or camera classe
		self.s.close()
		self.config["IP"] = newIP
		self.main.save()
		self.modif_param()
		print("new IP set")

	def set_port(self, newport):#function to change port of sawyer or camera classe 
		self.s.close()
		self.config["port"] = newport
		self.main.save()
		self.modif_param()
		print("new port set")

	def send_msg(self, msg):
		try:
			print("Sending to sawyer",msg)
			self.s.send(msg)
		except Exception,e:
			print "Error on socket send: ",e
			self.connection()

	def modif_param(self):
		self.connection()

	def stop(self):
		self.s.close()

	def connection(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.settimeout(0.3)
			print "Connecting..."
			self.s.connect((self.config["IP"], int(self.config["port"])))
			print("connected to %s:%s" % (self.config["IP"], self.config["port"]))
			self.connec_test = 1

		except Exception as e :
			print("something's wrong with %s:%s. Exception is %s" % (self.config["IP"], self.config["port"], e))
			self.connec_test = 0
			#time.sleep(1)

class Sawyer(Interface):
	def __init__(self,main, config,):
		Interface.__init__(self, main, config)
		self.connection()
		print "sawyer is initialising"

	def send(self, msg):
		try:
			if(self.connec_test == 1): #try the connection with the robot
				if len(msg)>0:
					self.send_msg(msg)
			else:
				pass
		except Exception,e:
			print e
			pass
		
		

class Camera(Interface):
 	def __init__(self,main , config):
		Interface.__init__(self,main,config)
		self.connection()
		print "camera is initialising"

	def socket_run(self):
		msg = ""
		while True :
			try:
				if(self.connec_test == 1):
					#take message
					#read byte by byte
					tmp = self.s.recv(1)
					if (tmp == ";"):  #wait frame end
						if(len(msg)>0):  #if message is not null
							self.process_msg(msg)
							msg = ""
					else : 
						msg += tmp
			except Exception,e:
				print e
				pass

#we devise data by 1000 but if data is inferior than 100 we suppose is an int variable (nb of objects detected..)
	def process_msg(self, msg):
		msg = msg.split(",")
		if (float(msg[0]) > 100):
			tmp = str(float(msg[0])/1000)
		else :
			tmp = str(int(msg[0]))
		for i in xrange(1,len(msg)):
			tmp += ","
			if (float(msg[i]) > 100):
				tmp += str(float(msg[i])/1000)
			else : 
				tmp = str(int(msg[i]))
			pass
		msg = tmp
		msg +=";"
		print(msg)
		self.main.sawyer.send(msg)
		

class Main():
	def __init__(self, path):
		self.path = path
		self.load()
		self.sawyer = Sawyer(self, self.config["sawyer"])
		self.camera = Camera(self, self.config["camera"])
		

	def load(self): #load dico with port and IP of Camera and robot
		print "loading"
		with open(self.path, 'r') as f_read :
			self.config = json.load(f_read)


	def save(self): #save on json file the IP and Port of Camera and robot
		print "saving"
		with open(self.path, 'w') as f_write :
			json.dump(self.config, f_write)

def main():
	#path of JSON file where are save IP and port of camera and sawyer
	path = "/home/pi/SawyerSensopart/param.json" 
	start = Main(path)

if __name__ == "__main__":
	main()	
