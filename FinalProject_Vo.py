#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 23:09:40 2024

@author: tandyllc
"""

""" Final Project: Password Generator """

import random

print("""
This is a password generator. It can give you two types of passwords. You can either have 1) a randomized set of letters,
symbols, and numbers OR  2) you can have strings put together with symbols and numbers. Please base your choice on the needs of the password.
      """)

while True:
    password_type = input("What type of password are you looking for? Enter '1' for option 1, and '2' for option 2: ")
    if password_type == "1":
        password_min = input("Enter the minimum number of characters you need for your password: ")
        if "-" in password_min:
            print("Minimum length must be a positive integer.")
            continue
        try:
           password_min = int(password_min)
        except:
            print("Invalid minimum. Must be positive whole number.") 
            continue
        password_max = input("Enter the maximum number of characters you want for your password: ")
        password_max = int(password_max)
        break
    elif password_type == "2":
        password_min = input("Enter the minimum number of characters you need for your password: ")
        password_max = input("Enter the maximum number of characters you want for your password: ")
        break
    else:
        print("Invalid option. Please select 1 or 2.")
        
password_length = random.randrange(password_min, password_max)

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
capital_alphabet = [letter.upper() for letter in alphabet]
digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
           '{', '}', '[', ']', ';', ':',  '<', '>', ',', '.',
           '?', '/', '~']

def option1():
    while True:
        password_length = random.randrange(password_min, password_max)
        password_list= []
        password_result = ""
        
        for i in range(1, password_length + 1):
            type_of_character = random.randrange(1,5)
            if type_of_character == 1:
                character = random.choice(alphabet)
            if type_of_character == 2:
                character = random.choice(capital_alphabet)
            if type_of_character == 3:
                character = random.choice(symbols)
            if type_of_character == 4:
                character = str(random.choice(digits))
            password_list.append(character)
        
        for i in password_list:
            password_result = password_result + i
        
        print(password_result)
        
        try_again = input("Press any key to exit. Press enter to create another password. ")
        if try_again:
            break
 
option1()
# Not sure how to code this yet, but writing my general ideas
        
# option 2 idea
# import the list of words created in TXT file, read into something
# if there is a way to organize and them randomize a number and select that corresponding number to the words in the txt file that is ideal
# ranodmize how many numbers and symbols are needed between 1-4
# keep making strings of words awith numbers and symbols at the end until we fit in the minimum and maximum
    # example if the first is RedFlamingoLion98$ but this is too many characters, then it can keep making randomized words until
    # RedDogPillow54#, which is shorter
    
# print back out to the user the result and ask if they like it
# do it again if they do not and keep if they do

# find a way to ask for email and email them when they next need to change the password??? If possible
