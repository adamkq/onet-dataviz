#str test

def nameRobotsFormat(s, d, maxlen=108, minlen=103):
	s = s.lower()
	for key in d:
		s = s.replace(key, d[key])

	if s[maxlen:].find("-") != -1: # clip to last word
		s = s[:maxlen + s[maxlen:].find("-")]
	
	while s.rfind("-") > minlen:
		s = s[:s.rfind("-")]
		
	if len(s) <= maxlen:
		return s

	# string must be within a certain len, but also have at least 2 letters in the last word.
	while s.rfind("-") < len(s) - 3 and len(s) >= minlen: 
		s = s[:-1]
	s += '-'
		
	return s

robots_url = "https://willrobotstakemyjob.com/"

prefix = "https://willrobotstakemyjob.com/53-3011-"

name = "agents-and-business-managers-of-artists-performers-and-athletes"
d = {",":"", "/":"", " ":"-"}

name = nameRobotsFormat(name, d, 108-len(prefix), 103-len(prefix))
s = prefix + name
print(s)


name = "Ambulance Drivers and Attendants, Except Emergency Medical Technicians"
name = nameRobotsFormat(name, d, 108-len(prefix), 103-len(prefix))
s = prefix + name
print(s)

name = "Combined Food Preparation and Serving Workers, Including Fast Food"
name = nameRobotsFormat(name, d, 108-len(prefix), 103-len(prefix))
s = prefix + name
print(s)

name = "Adult Basic and Secondary Education and Literacy Teachers and Instructors"
name = nameRobotsFormat(name, d, 108-len(prefix), 103-len(prefix))
s = prefix + name
print(s)
