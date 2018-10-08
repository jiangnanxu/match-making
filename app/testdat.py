import random

def generate(unique,username):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
	
    while True:
       
        value = "".join(random.choice(chars) for _ in range(5))
        email = value + "@gmail.com"
		      
	    
		
		
        if email not in unique:
            
            unique.append(email)
	
            
            
            break


def getuser(username):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
	
    while True:
       
        value = "".join(random.choice(chars) for _ in range(5))
        
		      
	    
		
		
        if value not in username:
            
            username.append(value)
	
            
            
            break			

def getstate(statechoicelist):
    statechoice=['VIC','NSW','QSL','SA','TAS','WA']
    
    while True:
        pickstate=random.choice(statechoice)
        statechoicelist.append(pickstate)	
        
        break


def getf(fmlist):
    fm=['f','m']
    
    while True:
        picks=random.choice(fm)
        fmlist.append(picks)	
        
        break


def geted(edulist):
    ed=['highschool','tertiary','master']
    
    while True:
        picked=random.choice(ed)
        edlist.append(picked)	
        
        break		

def geted(aglist):
    
    
    while True:
        pickint=random.randint(18,45)
        aglist.append(pickint)	
        
        break		


def getp(password):
   
	
    while True:
       
      
	    password.append("123")
	
            
            
            break
		
unique = ["hi","who","what"]
username=["yolo"]
password =["123"]
statechoicelist=['VIC']
fmlist=['f']
edulist=['highschool']
aglist=['20']


for _ in range(20):
    
	generate(unique,username)
    
	getstate(statechoicelist)
	getf(fmlist)
	geted(edulist)
	geted(aglist)
	getuser(username)
	getp(password)

print("email")	
print(unique)
print("password")
print(password)
print("statechoice")
print(statechoicelist)
print("gender choice")
print(fmlist)
print("education")
print(edulist)
print("age")
print(aglist)
print("usernam list")
print(username)



