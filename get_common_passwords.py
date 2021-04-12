import os
import hashlib
from hashlib import md5

keys_information = "key_log.txt"
file_path = os.getcwd()
keyLogs = open(os.path.join(file_path,keys_information), 'r')
keyLoggerWords = [word.split('\n') for word in keyLogs.readlines()]
keyLoggerDictionary = {}

for i in keyLoggerWords:
    SHA1 = hashlib.sha1()
    SHA1.update(i[0].encode('utf-8'))
    sha1String= SHA1.hexdigest()
    keyLoggerDictionary[sha1String] = i[0]

LeakedDatasetFile = open(os.path.join(file_path,"68_linkedin_found_hash_plain.txt"), 'r')
leakedPasswords = {}
print("Loading leaked passwords . .")
for password in LeakedDatasetFile:
    try:
        key, value = password.strip().split(':')
    except:
        continue
    leakedPasswords[key.strip()] = value.strip()

LeakedDatasetFile.close()
print("Checking in leaked passwords . . ")
for i in keyLoggerDictionary.keys():
    print(leakedPasswords.get(str(i)))
