#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 21:12:59 2024

@author: tandyllc
"""

""" Final Project: Password Generator """

import random
import pandas as pd
from flask import Flask, render_template, request, session
from matplotlib import pylab as plt
from datetime import date


app = Flask(__name__)
# Set a secret key for the application
app.secret_key = 'eece2140pythonproject'
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

# =============================================
# Global variables for use later
global global_email
global_email = ''
global questions_to_answer_to_get_passwords
questions_to_answer_to_get_passwords = {}
global answers_to_presented_questions
answers_to_presented_questions = []

# =============================================

# Extract security question answers
sec_questions = {
        1: 'What is the name of your childhood best friend?',
        2: 'In which city did your parents meet?',
        3: 'What was your first car brand?',
        4: 'What is a nickname you had at home?',
        5: 'What is the name of your first pet?',
        6: 'What is the maiden name of your grandmother?',
        7: 'What is the first concert you attended?',
        8: 'What was the name of your 7th grade history teacher?',
        9: 'What is your favorite film you saw in theaters?'
            }
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
            
        order_num_symb = random.choice([False, True])
        if order_num_symb:
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
        
# =============================================
# Append data to user_data list
def add_to_csv(email, final_password, security_answers):
    df = pd.read_csv('password_user_data.csv')
    all_stored_emails = df['User Email'].tolist()
    if email in all_stored_emails:
        current_num_passwords = all_stored_emails.count(email)
        current_num_passwords += 1
    else:
        current_num_passwords = 1
    password_date = date.today()
    # Initialize an empty data list
    new_data = {
        'User Email': email,
        'Index of password associated with this email': current_num_passwords,
        'Generated Password': final_password,
        'Date': password_date,
        **security_answers
    }
    # Convert user_data list to DataFrame
    df2 = pd.DataFrame([new_data])
    
    df = pd.concat([df, df2], ignore_index=True)
    
    df.to_csv('password_user_data.csv', index=False)

# =======================================================
def numbers_and_symbols(additives):

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
    
    return (need_symbols, need_numbers)

# =======================================================
@app.route('/', methods=['GET','POST'])
def password_generator():
    email = ''  
    final_password = ''  
    security_answers = {}  
    
    if request.method == 'POST':
        # Randomly choose three security questions
        three_questions = random.sample(list(sec_questions.items()), 3)
        
        try:
            email = request.form['email'].lower()
        except:
            email = None 
        try:
            password_type = request.form['option']
        except:
            no_entry = True  
            return render_template('password_generator.html', three_questions=three_questions, no_entry=no_entry)
        
        additives = request.form.getlist('additions')
        
        # Check for user number and symbols
        numbers_symbols = numbers_and_symbols(additives)
        
        if password_type == "random":
            # Call option1 function
            try:
                password_min = int(request.form['password_min'])
                password_max = int(request.form['password_max'])
            except:
                password_min = 10
                password_max = 16
            final_password = option1(password_min, password_max)
        
        elif password_type == "concat":
            # Call option 2 function
            try:
                password_min = int(request.form['password_min'])
                password_max = int(request.form['password_max'])
            except:
                password_min = 10
                password_max = 20
            final_password = option2(password_min, password_max, numbers_symbols[0], numbers_symbols[1]) 
        
        
        for question_num, question_text in sec_questions.items():
            answer = request.form.get(f'answer{question_num}')
            if answer:
                security_answers[question_text] = answer
            else:
                security_answers[question_text] = 'Not answered'
           
        if email and list(security_answers.values()).count('Not answered') == 6:
            save_success = add_to_csv(email, final_password, security_answers)
        else:
            save_success = False
            
        return render_template('password_generator.html', email=email, final_password=final_password, three_questions=three_questions, save_success=save_success)
    
    else:
        # Display the form with randomly selected questions
        three_questions = random.sample(list(sec_questions.items()), 3)
        
    
        return render_template('password_generator.html', three_questions=three_questions)

#==============================================
@app.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    questions_to_answer_to_get_passwords = {}
    answers_to_presented_questions = []
    if request.method == 'POST':
        global_email = request.form['forgot_pass_email'].lower()
        session['global_email'] = global_email
        saved_passwords = pd.read_csv('password_user_data.csv', header=0)
        user_entries = saved_passwords[saved_passwords['User Email'] == global_email]
        print("Global Email in forgot_pass:", global_email)
        print(user_entries)
        
        if not user_entries.empty:
            no_saved_passwords = False
            random_line = user_entries.sample(n=1)
            print("Random line:", random_line)  # Check random_line
            for question_num, question_text in sec_questions.items():
                answer = random_line[question_text].iloc[0]
                print("Answer for question", question_num, ":", answer)  # Check answer for each question
                if answer != 'Not answered':
                    questions_to_answer_to_get_passwords[question_num] = question_text
                    answers_to_presented_questions.append(answer)
            session['answers_to_presented_questions'] = answers_to_presented_questions
            session['questions_to_answer_to_get_passwords'] = questions_to_answer_to_get_passwords
            print("Questions to answer:", questions_to_answer_to_get_passwords)  # Check questions_to_answer_to_get_passwords
            print(answers_to_presented_questions)
            
                
            # Check if questions dictionary is empty
            if not questions_to_answer_to_get_passwords:
                no_questions = True
            else:
                no_questions = False
                
            return render_template('forgot_password.html', no_saved_passwords=no_saved_passwords, questions_to_answer_to_get_passwords=questions_to_answer_to_get_passwords, no_questions=no_questions, )

        else:
            no_saved_passwords = True
            print("no saved password")
            return render_template('forgot_password.html', no_saved_passwords=no_saved_passwords)
    else:
        return render_template('forgot_password.html')
            
# =============================================
@app.route('/get_passwords', methods=['GET','POST'])
def get_passwords():
   print_passwords = False
   global_email = session.get('global_email')
   answers_to_presented_questions = session.get('answers_to_presented_questions')
   questions_to_answer_to_get_passwords = session.get('questions_to_answer_to_get_passwords')
   print('passwords to present:' , answers_to_presented_questions)
   print("Global Email:", global_email)
   saved_passwords = pd.read_csv('password_user_data.csv', header=0)
   user_entries = saved_passwords[saved_passwords['User Email'] == global_email]
   print("User entries:", user_entries)
   print("Questions to answer:", questions_to_answer_to_get_passwords)
   
   if request.method == 'POST':
        answers_given = []
        for question_number, question_text in questions_to_answer_to_get_passwords.items():
            answer = request.form.get(f'get_pass_answer{question_number}', '')
            answers_given.append(answer)
        
        if answers_given == answers_to_presented_questions:
            print_passwords = True
            passwords_to_present = user_entries['Generated Password']
            print('passwords',passwords_to_present)
            return render_template('get_passwords.html', passwords_to_present=passwords_to_present, print_passwords=print_passwords, global_email=global_email, user_entries=user_entries)
        else:
            return render_template('get_passwords.html', message="Your answers do not match.", questions_to_answer_to_get_passwords=questions_to_answer_to_get_passwords)
   else:
        return render_template('get_passwords.html', questions_to_answer_to_get_passwords=questions_to_answer_to_get_passwords, global_email=global_email)

if __name__ == '__main__':
    app.run(debug=True)

# =============================================






