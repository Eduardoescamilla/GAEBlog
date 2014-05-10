from hashlib import sha256
from google.appengine.ext import db

keyword = "batata"

class User(db.Model):
	user = db.StringProperty(required = True)
	password = db.StringProperty(required = True)

def newUser(username, password):
	query = db.GqlQuery("SELECT * FROM User WHERE user = '%s'"%username)
	if query.get() != None:
		return None
	else:
		user = User(user = username, password = password)
		user = user.put()
		user_id = user.id()
		#TODO: Return cookie
		return createUserHash(user_id)

#def make_salt():
#    return ''.join(random.choice(string.letters) for x in xrange(5))


#def createHash(username, password, salt=None):
#	if salt = None:
#		salt = make_salt()
#	h = sha256(username+password+salt).hexdigest()
#	return '%s,%s' %(h, salt)
#def validateHash(username, password, h):
#	salt = h.split(',')[1]
#    return h == make_pw_hash(name, pw, salt)

def createUserHash(user_id):
	return str(user_id)+'|' + sha256(str(user_id) + keyword).hexdigest()

def validateUserHash(h):
	id = h.split('|')[0]
	if  h != createUserHash(id):
		return False
	user = User.get_by_id(int(id))
	
	return user.user
