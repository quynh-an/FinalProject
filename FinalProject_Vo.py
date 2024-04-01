#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 23:09:40 2024

@author: tandyllc
"""

""" Final Project: Password Generator """

import random
import pandas as pd
from flask import Flask, render_template, request
from matplotlib import pylab as plt
from datetime import datetime
# ==========================================
# List of symbols, digits, and alphabet
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
capital_alphabet = [letter.upper() for letter in alphabet]
digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
           '{', '}', '[', ']', ';', ':',  '<', '>', ',', '.',
           '?', '/', '~']
# ==========================================
# Show plot to show statistics of password security
sizes = [80, 20]  # Percentage values
labels = ['Cracked due to reuse, stolen, or weakness', 'Passwords which have not been cracked.' ]
colors = ['#1f77b4', '#ff7f0e']

# Create the pie chart
plt.figure(figsize=(7, 7))  # Set the size of the pie chart
plt.pie(sizes, labels = labels, colors=colors, startangle=90)

# Add a title
plt.title('Percent of people who have had passwords cracked.')

# Display the pie chart
plt.show()

# ============================================
# Sample data
data = {
    'User Email': [],
    'Generated Password': [],
    'Date': [],
    'What is the name of your childhood best friend?': [],
    'In which city did your parents meet?': [],
    'What was your first car brand?': [],
    'What is a nickname you had at home?': [],
    'What is the name of your first pet?': [],
    'What is the maiden name of your grandmother?': [],
    'What is the first concert you attended?': []
}

# Create DataFrame
user_data = pd.DataFrame(data)

print(user_data)
# ============================================

# Option 1 for Passwords
def option1(password_min, password_max):
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
 
        return password_result
    
#Option 2 for Passwords
def option2(password_min, password_max):
    words_to_choose = []
    with open('password_nouns.txt', 'r') as password_words_file:
    # Read the file
       words = password_words_file.read()
       words_to_choose = words.splitlines()
       
    need_symbols = input("Do you need symbols in your password? Enter 'y' for yes. Any other key is no. ")
    need_numbers = input("Do you need numbers in your password? Enter 'y' for yes. Any other key is no. ")
    password_length = random.randrange(password_min, password_max)
    print(password_length)
    
    while True:
        while True:
            password_words= []
            password_result = ""
            num_words_in_pass = random.randrange(1, 4)
            
            password_result = ""
            for i in range(num_words_in_pass):
                choice_word = random.choice(words_to_choose)
                cap = random.choice([False, True])
                if cap:
                    word_to_add = choice_word.capitalize()
                else:
                    word_to_add = choice_word
                password_words.append(word_to_add)
                
            num_symb = cap = random.choice([False, True])
            if num_symb:
                if need_symbols.lower() == 'y':
                    num_symbols = random.randint(1,2)
                    for i in range(num_symbols):
                        symbol = random.choice(symbols)
                        password_words.append(symbol)
                    
                if need_numbers.lower() == 'y':
                    num_nums = random.randint(1,3)
                    for i in range(num_nums):
                        number = str(random.choice(digits))
                        password_words.append(number)
            else:
                if need_numbers.lower() == 'y':
                    num_nums = random.randint(1,3)
                    for i in range(num_nums):
                        number = str(random.choice(digits))
                        password_words.append(number)
                    
                if need_symbols.lower() == 'y':
                    num_symbols = random.randint(1,2)
                    for i in range(num_symbols):
                        symbol = random.choice(symbols)
                        password_words.append(symbol)
                        
            
            for i in password_words:
                password_result = password_result + i
            
            if len(password_result) == int(password_length):
                break
        
        print(password_result)
        
        try_again = input("Type 'y' to continue generating another password. Press any other key to exit.")
        if try_again != 'y':
            break
        
        return password_result
    
def main():
    print("""
    This is a password generator. It can give you two types of passwords. You can either have 1) a randomized set of letters,
    symbols, and numbers OR  2) you can have strings put together with symbols and numbers. Please base your choice on the needs of the password.
         """)
    
    while True:
        
        # Ask for user email and get a date
        email = input("First, enter an email: ")
        date = datetime.now()
        
        password_type = input("What type of password are you looking for? Enter '1' for option 1, and '2' for option 2: ")
        if password_type == "1":
            password_min = input("Enter the minimum number of characters you need for your password. Best passwords are > 8: ")
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
            final_password = option1(password_min, password_max)
            break
        elif password_type == "2":
            while True:
                try:
                    print("You'll be asked for the minimum and maximum character for your password. If you have no answer, leave it blank.")
                    password_min = input("Enter the minimum number of characters you need for your password. Best passwords are > 8: ")
                    password_max = input("Enter the maximum number of characters you want for your password: ")
                    if password_min == "":
                        password_min = 12
                    else:
                       password_min = int(password_min)
                    if password_max == "":
                        password_max = 20
                    else:
                        password_max = int(password_max)
                    final_password = option2(password_min, password_max)
                    break
                except ValueError:
                    print("Enter only an integer number of characters.")
            break
        else:
            print("Invalid option. Please select 1 or 2.")
            
    security_data = security_questions()
        
    new_data = {
        'User Email': email ,
        'Generated Password': final_password,
        'Date': date,
        'What is the name of your childhood best friend?': security_data[0][1],
        'In which city did your parents meet?': security_data[1][1],
        'What was your first car brand?': security_data[2][1],
        'What is a nickname you had at home?': security_data[3][1],
        'What is the name of your first pet?': security_data[4][1],
        'What is the maiden name of your grandmother?': security_data[5][1],
        'What is the first concert you attended?': security_data[6][1]
        }
            
    print(new_data)
    
def security_questions():
    security_questions_answers = []
    want_questions = input("Would you like to add security questions? If yes, enter 'y': ")
    
    if want_questions.lower() == 'y':
        questions = {
            1: "What is the name of your childhood best friend?",
            2: "In which city did your parents meet?",
            3: "What was your first car brand?",
            4: "What is a nickname you had at home?",
            5: "What is the name of your first pet?",
            6: "What is the maiden name of your grandmother?",
            7: "What is the first concert you attended?"
        }
    
        # Shuffle the order of questions
        shuffled_questions = list(questions.items())
        random.shuffle(shuffled_questions)
    
        for question_number, question_text in shuffled_questions:
            answer = input(f"{question_text}: ")
            if answer:
                security_questions_answers.append((question_number, answer))
            else:
                security_questions_answers.append((question_number, ""))
            
            addtl_questions = input("Would you like to add another security question? If yes, enter 'y': ")
            if addtl_questions.lower() != 'y':
                break
          
        # Check if all questions have been answered
        for question_number, _ in questions.items():
            if not any(q[0] == question_number for q in security_questions_answers):
                security_questions_answers.append((question_number, ""))
        
    security_questions_answers = sorted(security_questions_answers)

    print(security_questions_answers)
        

    return security_questions_answers 
     
main()      
            



# Option 3 Most Memorable using Personal Questions
    

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
# Use pandas to create a database
# Ask for the user emails when they get their password if they want to be reminded
# make csv file and save with pandas in a dataframe to calculate the time based on the date of password entry
# create a time since email and function that checks its limit and then call function to send an email
# I have to look into services to send emails

# Use flask to have a UI platform
# Use data visualizations to show maybe statistics on password protection just to use more of what we learned in class
# I can also use pandas for password verification questions

