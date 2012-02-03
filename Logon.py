import subprocess
import sys
import re
import os
from datetime import date

def runCommand(cmd):
	sys.stderr = sys.stdout
	print cmd
	proc = error=subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0].decode("windows-1252")
	return_code = proc.wait()
	output = ""
	for line in proc.stdout:
		output = output + "stdout: " + line.decode("windows-1252").rstrip() + "\n"
	for line in proc.stderr:
		output = output + "stderr: " + line.decode("windows-1252").rstrip() + "\n"
	return output
	pass
	

def disconnectDrives():
	print ("Disconnecting existing drives...");
	#cmd = "net use * /delete /yes"
	#runCommand(cmd)
	
def mapDrive(driveLetter, server, share, username, password):
	# map drive
	note = ("Loading " + driveLetter + " drive:  ")
	home = os.getenv('USERPROFILE') or os.getenv('HOME')
	networkDir = home + "NetworkDrives/"
	
	# If we're on Linux
	if sys.platform == "linux2":
		directory = networkDir + driveLetter
		if not os.path.exists(directory):
			os.makedirs(directory)
		cmd = "mount.cifs //" + server + "/" + share + " " + directory + " -o user=" + username + ",pass=" + password
		output = runCommand(cmd)
		print output

	# If we're on Windows
	elif sys.platform == "win32": 
		cmd = "net use " + driveLetter + ": \\\\" + server + "\\" + share + " /user:" + username + " " + password + " /PERSISTENT:No"
		output = runCommand(cmd)
		if 'success' in output:
	    		result = "SUCCESS"
		elif 'denied' in output:
				result = "DENIED"
		elif "not found" in output:
				result = "NOTFOUND"
		else:
				result = "FAILEDUNKNOWN"
	
	# If we're on OSX
	elif sys.platform == "darwin":
		directory = networkDir + driveLetter
		if not os.path.exists(directory):
			os.makedirs(directory)
		cmd = "mount_smbfs //" + username + ":" + password + "@" + server + "/" + share + " " + directory
		output = runCommand(cmd)
		print output
	#
	

def connectToPWSDrives(username, password):
	# Ensure all previous drives are disconnected
	disconnectDrives()

	yearGroupAtEnd = re.compile('.*([0-9]{4})$')
	match = yearGroupAtEnd.match(username)
	if match:
		graduatingyear = match.group(1)
		# To get yeargroup, 
		# Someone in year 12 in 2013 would be in year 11 if the current year is 2012
		# 11 = 2012 - 2013 + 12
		# yeargroup = currentyear - graduatingyear + 12
		currentyear = date.today().year
		yeargroup = int(currentyear) - int(graduatingyear) + 12
		connectToStudentPWSDrives(username, password, yeargroup)
	else:
		connectToStaffPWSDrives(username, password)

def connectToStaffPWSDrives(username, password):
	mapDrive("H", "192.168.0.5", username, username, password);
	mapDrive("X", "192.168.0.5", "xdrive", username, password);
	mapDrive("O", "192.168.0.5", "office", username, password);
	mapDrive("S", "192.168.55.1", "allstudents", username, password);
	mapDrive("Y", "192.168.55.1", "allsubjects", username, password);
	mapDrive("M", "192.168.0.5", "mailmerge", username, password);
	mapDrive("P", "192.168.0.5", "deputy", username, password);
	mapDrive("Q", "192.168.0.5", "payroll", username, password);
	mapDrive("R", "192.168.0.5", "accounts", username, password);
	mapDrive("W", "192.168.0.5", "seniorstaff", username, password);
	# Maze drive?  How can we map, only if one of the preceeding worked?  Say, office

	print ("Done");

def connectToStudentPWSDrives(username, password, yeargroup):
	print ("Disconnecting existing drives...");
	ydrive = str(yeargroup).zfill(2);
	print ydrive
	#disconnectDrives()
	#mapDrive("S", "192.168.55.1", username, username, password);
	#mapDrive("Y", "192.168.55.1", yeargroup, username, password);
	
	print ("Done");