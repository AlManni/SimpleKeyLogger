# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 17:07:08 2023

@author: NicholasMandelli
"""

import re

def analisi(filename):
    flagCard = 0
    flagCredential = 0
    # Open the file containing the stopwords list (Italian and English)
    with open('Stopwords.txt') as filesw:
        stopwords = filesw.read().splitlines()
    
    # Open the file that is recived for being analyzed
    with open(filename,encoding='utf-8', errors='ignore') as fTest:
        text = fTest.read()
    
    # Split the text in single words to analyze them
    words = text.split()
    
    # Remove from the text all the stopwords that are inside the stopwords file
    clean_words = [word for word in words if word not in stopwords]
    
    # Create a new file lighter then the first one (No stopwords inside the file)
    clean_text = ' '.join(clean_words)
    
    
    
    # Searching every single important element in the file
    with    open('Emails.txt', 'a') as femails, \
            open('Ibans.txt', 'a') as fIBAN, \
            open('Passwords.txt', 'a') as fpasswords, \
            open('Credit_Cards.txt', 'a') as fcards, \
            open('Credentials.txt', 'a') as fcredentials, \
            open('Results.txt', 'a') as fresult:
                
            
            #[0-9a-zA-Z]
        for line in clean_words:
            line = line.strip()
            emails = re.findall("[A-Za-z0-9]+[.-_]*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[0-9a-zA-Z]{2,})", line) # Email Search -> With this filter we can search every email, not only the ones with commons domains.
            ibanregistry = re.findall(r"\b[A-Z]{2}\d{2}[A-Z\d]{1,30}\b", line) # IBAN Search -> With this filter we can basically find every global standard IBAN
            complexPassword = re.findall(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!?b @#/\//€$%^§&+=]).*$', line) # Complex password Search-> With this filter we can search complex Password (Password that are made with high security standards)
            notComplexPassword = re.findall (r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$',line) # Not-Complex password Search -> With this filter we can search less complex Password (Passowrd made by only words and number)
            longcards = re.findall(r'^[0-9]{23,25}', line) # Cards Search -> With this filter we can search credit cards that were compiled without using "/" or tab/enter after every part (So a single long number of 23 to 25 digits)
            cards = re.findall(r'^[0-9]{16}', line) # Card Search -> With this filter we can search all the credit cards number in the file (We find only the 16 number of the card)
            expdates = re.findall(r'\d{2}/\d{2,4}',line) # Expire Date Search -> With this filter we can search all the expire date in the file (We will find also all the dates in the file but if a date is found after a 16 digit number is probably an expire date)
            secCodes = re.findall(r'\d{3}', line) # Security code Search -> With this filter we can search all the Security code (As for the Expire date we will need to see if the 3 digits came after a 16 digits and a 4/6 digits number or if it's a random 3 digit number)
            
            # Starting the printing phase for every match in the file
            # To be able to keep the time order of the matches in the file, every single time a match is found is printed in the correct file
            
            if(emails):
                email= emails
                femails.write(str(email[0])+'\n')
                fresult.write(str(email[0])+'\n')
                flagCard=0 # reset of the flag at 0 (if a mail is found, the card number,expire date or security code that is found is not near the other two information )
                flagCredential=1 # set of the Flag for Credentia file to 1 (if a password is the next "word" in the file we save both in the credential file)
               
                #print(email)
                
            elif(ibanregistry):
                iban= ibanregistry
                fIBAN.write(str(iban[0])+'\n')
                fresult.write(str(iban[0])+'\n')
                flagCard=0 # reset of the flag at 0 (if an IBAN is found, the card number,expire date or security code that is found is not near the other two information )
                flagCredential=0
                
               # print(iban)
                
            elif(complexPassword):
                password = complexPassword
                fpasswords.write(str(password[0])+'\n')
                fresult.write(str(password[0])+'\n')
                flagCard=0 # reset of the flag at 0 (if a password is found, the card number,expire date or security code that is found is not near the other two information )
                if flagCredential==1: # if this password is found after an email then we save both in the credentials file
                    fcredentials.write(str(email[0])+' '+str(password[0])+'\n')
                    flagCredential=0
                
                #print(password)
                
            elif(notComplexPassword):
                password2 = notComplexPassword
                fpasswords.write(str(password2[0])+'\n')
                fresult.write(str(password2[0])+'\n')
                flagCard=0 # reset of the flag at 0 (if a password is found, the card number,expire date or security code that is found is not near the other two information )
                if flagCredential==1: # if this password is found after an email then we save both in the credentials file
                    fcredentials.write(str(email[0])+' '+str(password[0])+'\n')
                    flagCredential=0
                    
               # print(password2)
                
            # If a credit card without spaces or "/" is found, this need to be written in a readable way
            elif(longcards):
                card = longcards[0] 
                if (len(longcards[0])==23): # We need to check if the expiring date is written in mm/yy or mm/yyyy 
                    fcards.write(str(card[0:16])+' '+str(card[16:18])+'/'+str(card[18:20])+' '+str(card[20:])+'\n') # For mm/yy we will have 23 digits that we need to separate as this
                    
                else: 
                    fcards.write(str(card[0:16])+' '+str(card[16:18])+'/'+str(card[18:22])+' '+str(card[22:])+'\n') # For mm/yyyy we will have 25 digits that we need to separate as this
                    
                flagCard=0 # reset of the flag at 0 (if a complete card is found, the card number,expire date or security code that is found is not near the other two information )
                flagCredential=0
               # print(card)
                
            elif(cards):
                card = cards
                #fcards.write(str(card)+'\n')
                flagCard+=1 # you add +1 to the flag as we are maybe finding something that could be a card written as 3 "words"
                
                flagCredential=0
                #print(card)
                
            elif(expdates):
                expdate = expdates
                #fcards.write(str(expdate)+'\n')
                flagCard+=1 # you add +1 to the flag as we are maybe finding something that could be a card written as 3 "words"
                
                flagCredential=0
                #print(expdate)
                
            elif(secCodes):
                secCode = secCodes
                if flagCard==2: # if the flag is ==2, it means that the last 2 "words" are a card number with the other information, otherwise is a random 3 digits number found in the file
                    fcards.write(str(card[0])+' '+str(expdate[0])+' '+str(secCode[0])+'\n')
                #fcards.write(str(secCode)+'\n')
                flagCredential=0
               #print(secCode)
                            
    # The file without stopwords is closed and saved, ready to be updated in the future with some text stolen by the software itself
    with open('Fetched_File.txt', 'w') as ffetched:
        ffetched.write(clean_text)
    print("File completato")
    fTest.close()
    
    
    # Print (clean_text)
