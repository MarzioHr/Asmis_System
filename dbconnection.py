from cryptography.fernet import Fernet 
import mysql.connector

# Try retrieving the Fernet encryption key
try:
  loginFRetrieve = open("key.bin", "rb")  # Retrieving Encryption key from file
  retrievedKey = loginFRetrieve.read()
  loginFRetrieve.close()
except:
  print("Error retrieving key.")
  
# Try retrieving the MySQL creds
try:
  loginFRetrieve = open("credentials.bin", "rb")  # Retrieving MySQL server login credentials
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
  # print("host="+splitCreds[0]+", user="+splitCreds[1]+", password="+splitCreds[2])
  mydb = mysql.connector.connect(host=splitCreds[0],user=splitCreds[1],password=splitCreds[2],database=splitCreds[3])
except:
  print("MySQL connection failed.")