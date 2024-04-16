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
    # randomize password length given input
    password_length = random.randrange(password_min, password_max)
    # make list for password parts
    password_list= []
    password_result = ""
    
    # iteratre through the randomized length of password
    for i in range(1, password_length + 1):
        # randomize a type of character
        type_of_character = random.randrange(1,5)
        # if 1, then lowercase, if 2 uppercase, if 3 symbol, if 4, digit
        if type_of_character == 1:
            character = random.choice(alphabet)
        if type_of_character == 2:
            character = random.choice(capital_alphabet)
        if type_of_character == 3:
            character = random.choice(symbols)
        if type_of_character == 4:
            character = str(random.choice(digits))
        # add the randomized character to a list
        password_list.append(character)
    # iteratre through that list of characters
    # add them together to make a random string of characters
    for i in password_list:
        password_result = password_result + i
 
    return password_result
 
# ============================================

# Option 2 for Passwords - Word concatenation
def option2(password_min, password_max, need_numbers, need_symbols):
    words_to_choose = []
    with open('password_nouns.txt', 'r') as password_words_file:
    # Read the file
       words = password_words_file.read()
       # make list of words to choose from the txt of words
       words_to_choose = words.splitlines()
    # determine a length for the password
    password_length = random.randint(password_min, password_max)

    while True:
        password_words= []
        password_result = ""
        # randomize a number of words to concatenate
        num_words_in_pass = random.randrange(2, 4)
        
        password_result = ""
        
        for i in range(num_words_in_pass):
            # choose words in the list of words
            choice_word = random.choice(words_to_choose)
            cap = random.choice([False, True])
            # if cap is true or false, capitalize the chosen words or not
            if cap:
                word_to_add = choice_word.capitalize()
            else:
                word_to_add = choice_word
            
            # add the words together
            password_words.append(word_to_add)
        
        # Randomize choice of true or false
        # if true, concatenation will be symbols then numbers at the end of a password
        # and if false, then the other way around (numbers then symbols)
        order_num_symb = random.choice([False, True])
        if order_num_symb:
            if need_symbols == True:
                # randomize choosing 1 or 2 symbols
                num_symbols = random.randint(1,2)
                for i in range(num_symbols):
                    # randomize symbols choice
                    symbol = random.choice(symbols)
                    # add the symbol/number to the password words list
                    password_words.append(symbol)
                
            if need_numbers == True:
                # randomize choosing 1 to 3 numbers
                num_nums = random.randint(1,3)
                for i in range(num_nums):
                    # randomize digits choice
                    number = str(random.choice(digits))
                    # add the symbol/number to the password words list
                    password_words.append(number)
        else:
            if need_numbers == True:
                num_nums = random.randint(1,3)
                for i in range(num_nums):
                    # randomize digits choice
                    number = str(random.choice(digits))
                    # add the symbol/number to the password words list
                    password_words.append(number)
                
            if need_symbols == True:
                num_symbols = random.randint(1,2)
                for i in range(num_symbols):
                    # randomize symbols choice
                    symbol = random.choice(symbols)
                    # add the symbol/number to the password words list
                    password_words.append(symbol)                   
        
        # for each password word, add them together to make the resulting concatenation
        for i in password_words:
            password_result = password_result + i
        
        # if the length of the password is what was made, then return, otherwise, try again until made!
        if len(password_result) == int(password_length):
            return password_result
        
# =============================================
# Append data to user_data list
def add_to_csv(email, final_password, security_answers):
    # made dataframe from csv
    df = pd.read_csv('password_user_data.csv')
    # put all emails into a list
    all_stored_emails = df['User Email'].tolist()
    # if the email is already in the list of stored emails, then increase a number of created passwords
    if email in all_stored_emails:
        current_num_passwords = all_stored_emails.count(email)
        current_num_passwords += 1
    # otherwise, start the number of passwords an email has to be 1
    else:
        current_num_passwords = 1
    # find today's date
    password_date = date.today()
    
    # Initialize an empty data list
    # add email, number of passwords, password, and date and security answers to the dataframe
    new_data = {
        'User Email': email,
        'Index of password associated with this email': current_num_passwords,
        'Generated Password': final_password,
        'Date': password_date,
        **security_answers
    }
    # Convert user_data list to DataFrame
    df2 = pd.DataFrame([new_data])
    
    # add the dataframes together (existing and new input)
    df = pd.concat([df, df2], ignore_index=True)
    
    # turn into CSV
    df.to_csv('password_user_data.csv', index=False)

# =======================================================
def numbers_and_symbols(additives):
    # thi function determines if the user inputs digits or symbols in their form and how to take care of it
    # if they want both, then both are true, not both, both are false, and then cases for one of each
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
        
    # return a tuple of booleans of if the password wanted numebrs and/or symbols
    return (need_symbols, need_numbers)

# =======================================================
@app.route('/', methods=['GET','POST'])
def password_generator():
    # password generator flask app route
    # initialize email, final password, and security answers
    email = ''  
    final_password = ''  
    security_answers = {}  
    
    # if information is input in HTML format:
    if request.method == 'POST':
        # Randomly choose three security questions
        three_questions = random.sample(list(sec_questions.items()), 3)
        # try to convert the email to lowercase
        # if not possible, email = None, which means that it won't save anyways down the line
        try:
            email = request.form['email'].lower()
        except:
            email = None 
        # get the type of password the user wants: concatenation or random
        try:
            password_type = request.form['option']
        except:
            no_entry = True  
            # if nothing is chosen and they press submit, then tell them they cannot make a password
            return render_template('password_generator.html', three_questions=three_questions, no_entry=no_entry)
        # get the additives from the form (symbol or digit)
        additives = request.form.getlist('additions')
        
        # call function to check which numbers and symbols the user wanted
        numbers_symbols = numbers_and_symbols(additives)
        
        # if the user selected password type random
        if password_type == "random":
            # Call option 1 function for randomizing
            try:
                # use input from form for minimum and maximum lengths
                password_min = int(request.form['password_min'])
                password_max = int(request.form['password_max'])
            except:
                # if none is included for minimum and maximum, then set them
                password_min = 10
                password_max = 16
                
            # call the make password function for optin 1 randomizer
            # set the final password to the result of option1
            final_password = option1(password_min, password_max)
        
        # if the concatenation type is selected
        elif password_type == "concat":
            # Call option 2 function
            try:
                # use input from form for minimum and maximum lengths
                password_min = int(request.form['password_min'])
                password_max = int(request.form['password_max'])
            except:
                # if none is included for minimum and maximum, then set them
                password_min = 10
                password_max = 18
                
            # call the make password function for option 2 concatenation
            # set the final password to the result of option2
            # include the numbers or sumbols booleans to get randomized order and choise of numbers and symbols
            final_password = option2(password_min, password_max, numbers_symbols[0], numbers_symbols[1]) 
        
        # for each question in the security questions dictionary:
        for question_num, question_text in sec_questions.items():
            # the answer comes from the security questions answers of the HTML
            answer = request.form.get(f'answer{question_num}')
            # if the answer is there, add to the dictionary the question and its answer
            # if the question did not even appear, then input the dictionary 'not answered'
            if answer:
                security_answers[question_text] = answer
            else:
                security_answers[question_text] = 'Not answered'
        
        # if the email was input correctly and there are 3 security questions (measured by how three are presented and
        # nine exist, which means 6 are 'not answered'
        if email and list(security_answers.values()).count('Not answered') == 6:
            save_success = True
            # call the add_to_csv function to store the password
            save_success = add_to_csv(email, final_password, security_answers)
        else:
            save_success = False
        
        # create the HTML with the questions, save success (if email and sec answers, etc)
        return render_template('password_generator.html', email=email, final_password=final_password, three_questions=three_questions, save_success=save_success)
    
    else:
        # Display the form with three randomly selected questions whenever the page is opened 
        three_questions = random.sample(list(sec_questions.items()), 3)
        # Display the form with the three random questions
        return render_template('password_generator.html', three_questions=three_questions)

#==============================================
@app.route('/forgot_password', methods=['GET','POST'])
# app route if you forgot your password
def forgot_password():
    # empty dictionary for security questions
    # empty list for predetermined answers to those questions
    questions_to_answer_to_get_passwords = {}
    answers_to_presented_questions = []
    # if the HTML if filled out
    if request.method == 'POST':
        # user input for emai;
        global_email = request.form['forgot_pass_email'].lower()
        # start a session for the email
        session['global_email'] = global_email
        # read the csv of passwords as a dataframe
        saved_passwords = pd.read_csv('password_user_data.csv', header=0)
        # filter the csv dataframe by user email
        user_entries = saved_passwords[saved_passwords['User Email'] == global_email]
        
        # if there are user entries in that filtered dataframe
        if not user_entries.empty:
            # variable to indicate there are no passwords is false
            no_saved_passwords = False
            # with saved passwords for thsat email, take a sample of one of them
            random_line = user_entries.sample(n=1)
            # for every question iterate through
            for question_num, question_text in sec_questions.items():
                # find the answer to the current security question
                answer = random_line[question_text].iloc[0]
                # if the answer is not indicated as unanswered, append it to a list of answers
                if answer != 'Not answered':
                    # Store the questions and answers to be answered for that email
                    questions_to_answer_to_get_passwords[question_num] = question_text
                    answers_to_presented_questions.append(answer)
            # store the questions and answers in a session
            session['answers_to_presented_questions'] = answers_to_presented_questions
            session['questions_to_answer_to_get_passwords'] = questions_to_answer_to_get_passwords
            
                
            # Check if questions dictionary is empty
            if not questions_to_answer_to_get_passwords:
                # if there are no questions to answer, then indicate that
                no_questions = True
            else:
                # if there are questions to answer, indicate this
                no_questions = False
            # Render the template with the variables below
            return render_template('forgot_password.html', no_saved_passwords=no_saved_passwords, questions_to_answer_to_get_passwords=questions_to_answer_to_get_passwords, no_questions=no_questions, )

        else:
            # if there were no user entries in the dataframe, then indicate there were no saved passwords
            no_saved_passwords = True
            return render_template('forgot_password.html', no_saved_passwords=no_saved_passwords)
    else:
        # if there was no user entry at all, render the template
        return render_template('forgot_password.html')
            
# =============================================
@app.route('/get_passwords', methods=['GET','POST'])
def get_passwords():
    # initialize variable to indicate if the passwords have been printed or not
   print_passwords = False
   # retriev email from the session
   # retrieve answers to the security questions and the questions to answer in the session
   global_email = session.get('global_email')
   answers_to_presented_questions = session.get('answers_to_presented_questions')
   questions_to_answer_to_get_passwords = session.get('questions_to_answer_to_get_passwords')
   # open the CSV and read it
   saved_passwords = pd.read_csv('password_user_data.csv', header=0)
   # filter the dataframe based on the user email
   user_entries = saved_passwords[saved_passwords['User Email'] == global_email]
   
   # if the HTML was submitted
   if request.method == 'POST':
       # minitialize answers list
        answers_given = []
        # Iterate through the questions to answer to retrieve the passwords
        for question_number, question_text in questions_to_answer_to_get_passwords.items():
            # get the answer from the HTML from the user's input
            answer = request.form.get(f'get_pass_answer{question_number}', '')
            answers_given.append(answer)
        
        # Check if the answers given by the user are what are stored
        if answers_given == answers_to_presented_questions:
            # if the answers given are the same as what was entered:
            print_passwords = True
            # once the print passwords is true, the user cannot try again to answer the security questions
            passwords_to_present = user_entries['Generated Password']
            # return template
            return render_template('get_passwords.html', passwords_to_present=passwords_to_present, print_passwords=print_passwords, global_email=global_email, user_entries=user_entries)
        else:
            # the answers do not match the answers input earlier
            # return template
            return render_template('get_passwords.html', message="Your answers do not match.", questions_to_answer_to_get_passwords=questions_to_answer_to_get_passwords)
   else:
       # if not POST render the template 
        return render_template('get_passwords.html', questions_to_answer_to_get_passwords=questions_to_answer_to_get_passwords, global_email=global_email)

# Run the Flask app with debug mode on
if __name__ == '__main__':
    app.run(debug=True)

# =============================================