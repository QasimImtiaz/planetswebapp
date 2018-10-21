#imports
from flask import Flask, Response,url_for,abort, redirect, request, render_template, json, session, flash, logging 
import os
from planet import Planet

#app
app = Flask(__name__)
#\pp secret key
app.secret_key = 'A0Zr98j /3 yX R~XHH!jmN]LWX / ,? RT'

#shows the home template when you visit the homepage root
@app.route("/")
def index():
        
	return render_template('home.html')

       
@app.route("/dashboard")
def dashboard():
	#try and except
	try:
		#checks if user is logged in and then display the dashboard.html template
		if session['username']:
			return render_template('dashboard.html')
	except KeyError:
		pass
	#displayed when user not logged in
	return render_template('dashboardFailure.html')

'''
When user clicks on submit, it is checked that if both text boxes is filled in 
if not, error message is shown
if it is, checked if both username and  password is correct 
if username and password correct, user successfully logged in and redirects to the dashboard route
if not, error message is shown
'''
@app.route("/login", methods=['POST', 'GET'])
def login():
        if request.method == 'POST':
                if request.form['username'] != '' and request.form['password'] != '':
                        fRead = open("accounts.txt", "r")
                        accountsList = [account.split(",") for account in fRead.readlines()]

                        username = request.form['username']
                        password = request.form['password']

                        for accounts in accountsList:
                                for i in range(0, len(accounts)):
                                        if(accounts[i] == username and accounts[i+1] == password):
						session['logged_in'] = True
						session['username'] = username
                                                return redirect(url_for('.dashboard'))
						
                        return render_template('login.html') + "<br/>" + "<div align = 'center'> Error: Username or password is incorrect</div>"

                else:
                        return render_template('login.html') + "<br/>" + "<div align = 'center'> Error: One or more input boxes are not filled in</div>"
        else:

                return render_template('login.html')



'''
check if user is logged in 
if user is logged in, user can start filling in the boxes 
if user not logged in, user is redirected to login page 
when user clicks on the submit button, textboxes are checkd that its empty or not
if
r more  textboxes empty, error message is displayed
if the textboxes not empty, user have successfully uploaded planet
'''
@app.route("/uploadPlanet", methods=['POST', 'GET'])
def uploadPlanet():
	file = ''
	planetName = ''
	planetDescription = ''
	radius = ''
	surfacePressure = ''
	meanDensity = ''
	surfaceGravity = ''
	try:
		if session['username'] :


	
			planetId = 0
			if request.method == 'POST':


				if request.form['planetName'] != '' and request.form['planetDescription'] != '' and request.form['planetDescription'] and request.form['radius']!= '' and request.form['surfacePressure'] != '' and request.form['meanDensity'] != '' and request.form['surfaceGravity'] != '' and request.form['meanAnomaly'] != '' and request.form['interestingFact'] != '':
					planetId += 1
        				file = request.files['image']  
					file.save('static/' + file.filename)
					planetName = request.form['planetName']
					planetDescription = request.form['planetDescription']
					radius = request.form['radius']
					surfacePressure = request.form['surfacePressure']
					meanDensity = request.form['meanDensity']
					surfaceGravity = request.form['surfaceGravity']
					meanAnomaly = request.form['meanAnomaly']
					interestingFact = request.form['interestingFact']
		
					f = open("planetsFile.txt", "a")
					f.write('<img src=' + '"/static/' + str(file.filename) + '">' +  "," + "Name: " + str(planetName) + "," + "Description: " +  str(planetDescription) + "," + "Radius: " +  str(radius) + "," + "Surface Pressure: " + str(surfacePressure) + "," + "Mean Density: " + str(meanDensity) + "," + "Surface Gravity: " + str(surfaceGravity) + "," + "Mean Anomaly: " + str(meanAnomaly) + "," + "Interesting Fact: " + str(interestingFact) + ",")
		        
                                        userF = open(str(session['username']) + ".txt", "a")
					userF.write(str(planetId) + "," +  '"/static/' + str(file.filename) + '">' +  "," + "Name: " + str(planetName) + "," + "Description: " +  str(planetDescription) + "," + "Radius: " +  str(radius) + "," + "Surface Pressure: " + str(surfacePressure) + "," + "Mean Density: " + str(meanDensity) + "," + "Surface Gravity: " + str(surfaceGravity) + "," + "Mean Anomaly: " + str(meanAnomaly) + "," + "Interesting Fact: " + str(interestingFact) + ",")
					return render_template('uploadPlanetSuccess.html') 


		

		
				else:
					return render_template('uploadPlanetFailure.html')

			else:
				
				return render_template('uploadPlanet.html')
	except KeyError:
		pass
	return redirect(url_for('.login'))

'''
checks if user logged in 
if user is not logged in, error message is displayed
if user logged in, user is signed out 
'''
@app.route("/signout/")
def signout():
	try:
		if session['username']:
			session.pop('username', None)
			session.pop('password', None)
			return render_template("signout.html")

	except KeyError:
        	 pass

		

	return render_template("signoutFailure.html")
	

@app.route("/displayPlanets/")

def display():
	# open json file and load it 
	with open('planets.json') as f:
		data = json.load(f)
		
	result = ''
	result2 = ''
	
	#loop through attributes of all  planets in the json file and append it to the result variable 
	for planet in data['planets']:
		start = '<img src="'
		url = url_for('static',filename=planet['image'])
		end = '">'
		result += start + url + end + "<br/>" +  "Name: " + str(planet['name']) + "<br/>Description: " +  str(planet["description"]) + "<br/>Radius: " + str(planet["Radius"]) + "<br/>Surface Pressure: " + planet["Surface Pressure"] + "<br/>Mean density: " + planet["Mean density"] + "<br/>Surface gravity: " + planet["Surface gravity"] + "<br/>Mean anomaly: " + planet["Mean anomaly"] + "<br/>Interesting fact:" + planet["InterestingFact"] + "<br/>" + "<br/>"
	        
	
	#open text file 
	textFile = open("planetsFile.txt",'r')
	
	#text between commas is put into a list 
	linesList = [line.split(",") for line in textFile.readlines()]

        result2 = ''
	#all value in list is looped through and appended to the result2 variable
        for line in linesList:
                for line2 in line:
                        result2 += line2 + "<br/>"

	#display 'displatPlanets.html' template and display planets afterwards 
	return render_template('displayPlanets.html') + "<div = align = 'center'>" + result + result2 + "</div>"
	
'''
When user clicks on search button,
input box checked if it is empty or not
if input box is empty, error message is displayed
if input box not empty, checked if planet name is in json or text file
if it is, the planet values are all displayed
if not, error message is displayed
'''

@app.route("/searchPlanet/",methods=['POST','GET'])
def search():
	searched = False
	if request.method == 'POST':
		if request.form['planetName'] != '':
			result = render_template('searchPlanet.html') + "<br/>" + "<div align = 'center'>"

			planetName = request.form['planetName']
			textFile = open("planetsFile.txt",'r')
			linesList = [line.split(",") for line in textFile.readlines()]

           
			for line in linesList:
				for i in range(1, len(line)):
					if(line[i] == "Name: " + planetName):
						searched = True
					
						result += line[i-1] + "<br/>" + line[i] + "<br/>" + line[i+1] + "<br/>" + line[i+2] + "<br/>" +  line[i+3] + "<br/>" + line[i+4] + "<br/>" + line[i+5] + "<br/>" + line[i+6] + "<br/>" + line[i+7] + "<br/>"
		
			with open('planets.json') as f:
     				data = json.load(f)
			for planet in data["planets"]:
				if planet["name"] == planetName:
					searched = True
					start = '<img src="'
                			url = url_for('static',filename=planet['image'])
                			end = '">'

					result += start + url + end + "<br/>" + "Name: " + planet["name"] + "<br/>" + "Description: " + planet["description"] + "<br/>" + "Radius: " + planet["Radius"] + "<br/>" + "Surface Pressure: " + planet["Surface Pressure"] + "<br/>" + "Mean Density: " + planet["Mean density"] + "<br/>" + "Surface Gravity: " + planet["Surface gravity"] + "<br/>" + "Mean Anomaly: " + planet["Mean anomaly"] + "<br/>" + "Interesting Fact: " + planet["InterestingFact"] + "<br/>"
			if searched == False:
				result = render_template('searchPlanet.html') + " <div align = 'center'>" + "Planet is not found!" 	
			return result + "</div>"
		else:
			return render_template('searchPlanet.html') + "<div align = 'center'>" + "Input box is not filled in" + "</div>"
	else:
		
		return render_template('searchPlanet.html') 

'''
When user clicks on submit button, 
user is checked that he or she have filled in all of the input boxes
if user did not filled in all of the input boxes, error message is displayed
if user did filled in all of the input boxes, the email address and username both checked that is available 
if username and email address available, user successfully registered
if username and email address not available, error message is displayed 
'''
	
@app.route("/register/", methods=['POST','GET'])
def register():
	if request.method == 'POST':
		if request.form['username'] != '' and request.form['password'] != '' and request.form['email'] != '':
		
			
			fRead = open("accounts.txt", "r")
        		accountsList = [account.split(",") for account in fRead.readlines()]
			

			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			for accounts in accountsList:
				if username in accounts or email in accounts:
				
					return render_template('register.html') + "<br/>" + "<div align = 'center'>Error: Username or email already exists!</div>"
					
			fWrite = open("accounts.txt", "a")
                       	fWrite.write(username +  "," + password + "," + email + ",")
			return render_template('register.html') + "<br/>" + "<div align = 'center'>You have sccuessfully made an account!</div>"

		else:
		                                                 
			return render_template('register.html') + "<br/>" + "<div align = 'center'>Error: One or more input boxes are not filled in!'</div>"
			
		
	else:
		return render_template('register.html')


#error messages dsplayed if page not found:
@app.route('/force404')
def force404():
	abort(404)

@app.errorhandler(404)
def page_not_found(error):
	return	"Couldn't find the page you requested.", 404


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)

