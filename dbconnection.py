from cryptography.fernet import Fernet # lib to decrypt MySQL credentials from binary file
import mysql.connector # MySQL connector library

# Try retrieving the Fernet encryption key from bin file
try:
  loginFRetrieve = open("config/key.bin", "rb")
  retrievedKey = loginFRetrieve.read()
  loginFRetrieve.close()
except:
  print("Error retrieving key.")
  
# Try retrieving the MySQL credentials from bin file
try:
  loginFRetrieve = open("config/credentials.bin", "rb")
  retrievedCred = loginFRetrieve.read()
  loginFRetrieve.close()
except:
  print("Error retrieving credentials.")
  
# Decrypt the retrieved MySQL creds and split into list
cipher = Fernet(retrievedKey)
credential = cipher.decrypt(retrievedCred)
credential = credential.decode('utf-8')
splitCreds = credential.split(":")

# Try connecting to MySQL DB with decrypted credentials
try:
  mydb = mysql.connector.connect(host=splitCreds[0],user=splitCreds[1],password=splitCreds[2],database=splitCreds[3])
except:
  print("MySQL connection failed.")