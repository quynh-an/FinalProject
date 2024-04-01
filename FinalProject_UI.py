#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 21:12:59 2024

@author: tandyllc
"""

""" Final Project: Password Generator """

import random
import pandas as pd
from flask import Flask, render_template, request
from matplotlib import pylab as plt
from datetime import date
import csv

app = Flask(__name__)
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

# Option 1 for Passwords
def option1(password_min, password_max):
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
 
    return password_result
 
# ============================================

#Option 2 for Passwords
def option2(password_min, password_max, need_numbers, need_symbols):
    words_to_choose = []
    with open('password_nouns.txt', 'r') as password_words_file:
    # Read the file
       words = password_words_file.read()
       words_to_choose = words.splitlines()

    password_length = random.randint(password_min, password_max)

    while True:
        password_words= []
        password_result = ""
        num_words_in_pass = random.randrange(2, 4)
        
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
            if need_symbols == True:
                num_symbols = random.randint(1,2)
                for i in range(num_symbols):
                    symbol = random.choice(symbols)
                    password_words.append(symbol)
                
            if need_numbers == True:
                num_nums = random.randint(1,3)
                for i in range(num_nums):
                    number = str(random.choice(digits))
                    password_words.append(number)
        else:
            if need_numbers == True:
                num_nums = random.randint(1,3)
                for i in range(num_nums):
                    number = str(random.choice(digits))
                    password_words.append(number)
                
            if need_symbols == True:
                num_symbols = random.randint(1,2)
                for i in range(num_symbols):
                    symbol = random.choice(symbols)
                    password_words.append(symbol)                   
        
        for i in password_words:
            password_result = password_result + i
        
        if len(password_result) == int(password_length):
            return password_result
        

# =======================================================
# Extract security question answers
sec_questions = {
        1: 'What is the name of your childhood best friend?',
        2: 'In which city did your parents meet?',
        3: 'What was your first car brand?',
        4: 'What is a nickname you had at home?',
        5: 'What is the name of your first pet?',
        6:'What is the maiden name of your grandmother?',
        7: 'What is the first concert you attended?'
            }
# Initialize an empty DataFrame
user_data = []
# =============================================
@app.route('/', methods=['GET','POST'])
def password_generator():
    global user_data
    email = ''  # Initialize email outside the POST block
    final_password = ''  # Initialize final_password outside the POST block
    security_answers = {}  # Initialize security_answers outside the POST block
    password_date = date.today()
    
    if request.method == 'POST':
        try:
            email = request.form['email']
        except:
            email = None 
        password_type = request.form['option']
        additives = request.form.getlist('additions')
        # Extract other form fields as needed
        
        if 'symbols' in additives and 'digits' not in additives:
            need_symbols = True
            need_numbers = False
        
        elif 'digits' in additives and 'symbols' not in additives:
            need_numbers = True
            need_symbols = False
        
        elif 'digits' and 'symbols' in additives:
            need_symbols = True
            need_numbers = True
            
        elif 'digits' and 'symbols' not in additives:
            need_symbols = False
            need_numbers = False
        
        if password_type == "random":
            # Call option1 function
            password_min = int(request.form['password_min'])
            password_max = int(request.form['password_max'])
            final_password = option1(password_min, password_max)
        elif password_type == "concat":
            # Call option2 function
            password_min = int(request.form['password_min'])
            password_max = int(request.form['password_max'])
            final_password = option2(password_min, password_max, need_numbers, need_symbols) 
            
        # Randomly choose three security questions
        three_questions = random.sample(list(sec_questions.items()), 3)

        # Extract security question answers
        for question_num, question_text in sec_questions.items():
            answer = request.form.get(f'answer{question_num}')
            if answer:
                security_answers[question_text] = answer
            else:
                security_answers[question_text] = 'Not answered'
           
        
        # Append data to user_data list
        if email:
            password_date = date.today()
            new_data = {
                'User Email': email,
                'Generated Password': final_password,
                'Date': password_date,
                **security_answers
            }
            user_data.append(new_data)
            
            # Convert user_data list to DataFrame
            df = pd.DataFrame(user_data)
            df.to_csv('password_user_data.csv', index=False)
            
        return render_template('password_generator.html', email=email, final_password=final_password, three_questions=three_questions)
    
    else:
        # Display the form with randomly selected questions
        three_questions = random.sample(list(sec_questions.items()), 3)
    
        return render_template('password_generator.html', three_questions=three_questions)
    

if __name__ == '__main__':
    app.run(debug=True)
# =============================================

password_generator()





