from cryptography.fernet import Fernet

fopen = open("key.bin","rb")
key = fopen.read()
fopen.close()

fopen = open("clearinput.bin","rb")
cred = fopen.read()
fopen.close()

print("The Clear Input is:")
print(cred)

f = Fernet(key)
token = f.encrypt(cred)

print("The Encrypted Output is:")
print(token)

fopen = open("credentials.bin","wb")

fopen.write(token)
fopen.close()