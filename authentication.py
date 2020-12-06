import dbconnection
from argon2 import PasswordHasher  # Argon2 lib to hash password
  
# set DB cursor
mycursor = dbconnection.mydb.cursor()

# set Argon2 password hasher object
ph = PasswordHasher()

# use Argon2 to hash password and return hash as string
def hashPswd(password):
  hash = ph.hash(password)
  return hash

# userExists checks a database too see if username exists in the database
def userExists(user):
  mycursor.execute("SELECT username FROM logins WHERE username = '%s'" % user)
  userResult = mycursor.fetchall()
  if userResult:
    return True
  return False

# Creates a new user in the connected SQL database with given info and saves password as hash
def newUser(user, password, firstName, lastName):
  if userExists(user) == False:
    if (any(map(str.isdigit, password))==True) and (any(map(str.isalpha, password))==True) and (len(password)>=8):
      mycursor.execute("SELECT username FROM logins WHERE username = '%s'" % user)
      mycursor.fetchall()
      hashedPass = hashPswd(password)
      sql = "INSERT INTO logins(username, password, firstname, lastname) VALUES(%s,%s,%s,%s)"
      val = (user, hashedPass, firstName, lastName)
      mycursor.execute(sql, val)
      dbconnection.mydb.commit()
      print("\nUser created successfully. Please login with your credentials.")
      return True
    else:
      print("\nError: Please ensure that the password is atleast 8 characters long and includes both letters and numbers.")
      return False
  else:
    print("\nError: User exists already.")
    return False

# Checks the connected SQL database for an existing user.
def existingUser(user, password):
  if user != "":
    if userExists(user) == True:
      hashedPass = hashPswd(password)
      mycursor.execute("SELECT * FROM logins")
      passResult = mycursor.fetchall()
      for row in passResult:
        if row[1] == user:
          try: 
            if ph.verify(row[2], password) == True:
              print("\nLogin Successful. Welcome back to the ASMIS system, %s!" % row[3])
              return (row[0],row[1],row[3],row[4])
            else:
              print("\nLogin Error: Password does not match our records")
          except:
            print("\nLogin Error: Password does not match our records")
    else:
      print("\nLogin Error: User does not exist")
  else:
    print("\nLogin Error: Please enter a username")