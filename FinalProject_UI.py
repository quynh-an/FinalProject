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

    password_length = random.randrange(password_min, password_max)
    print(password_length)

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
            break
        
        return password_result

# =======================================================
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
                security_questions_answers.append((question_number, None))
        
    security_questions_answers = sorted(security_questions_answers)
        
    return security_questions_answers 

# ================================================
    
def main():

    # dataframe outline
    data = {
        'User Email': ['sample@gmail.com'],
        'Generated Password': ['MyPassword.123'],
        'Date': ['2024-31-03'],
        'What is the name of your childhood best friend?': ['Abby Smith'],
        'In which city did your parents meet?': ['New York'],
        'What was your first car brand?': ['Nissam Altima'],
        'What is a nickname you had at home?': ['Blue'],
        'What is the name of your first pet?': ['Spot'],
        'What is the maiden name of your grandmother?': ['Johnson'],
        'What is the first concert you attended?': ['One Direction']
    }

    # Create DataFrame
    user_data = pd.DataFrame(data)
    print("""
    This is a password generator. It can give you two types of passwords. You can either have 1) a randomized set of letters,
    symbols, and numbers OR  2) you can have strings put together with symbols and numbers. Please base your choice on the needs of the password.
         """)
    
    while True:
        
        # Ask for user email and get a date
        email = input("First, enter an email: ")
        password_date = date.today()
        
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
        'User Email': [email] ,
        'Generated Password': [final_password],
        'Date': [password_date],
        'What is the name of your childhood best friend?': [security_data[0][1]],
        'In which city did your parents meet?': [security_data[1][1]],
        'What was your first car brand?': [security_data[2][1]],
        'What is a nickname you had at home?': [security_data[3][1]],
        'What is the name of your first pet?': [security_data[4][1]],
        'What is the maiden name of your grandmother?': [security_data[5][1]],
        'What is the first concert you attended?': [security_data[6][1]]
        }
            
    user_data = pd.concat([user_data, pd.DataFrame(new_data)], ignore_index=True)
    
    print(user_data)


# =============================================
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
# =============================================
@app.route('/', methods=['GET','POST'])
def password_generator():
    email = ''  # Initialize email outside the POST block
    final_password = ''  # Initialize final_password outside the POST block
    security_answers = {}  # Initialize security_answers outside the POST block
    if request.method == 'POST':
        email = request.form['email']
        password_type = request.form['option']
        additives = request.form.getlist('additions')
        q1_answer = request.form['answer{{q1}}']
        q2_answer = request.form['answer{{q2}}']
        q3_answer = request.form['answer{{q3}}']
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
        q1 = three_questions[0][1]
        q2 = three_questions[1][1]
        q3 = three_questions[2][1]
    
        return render_template('password_generator.html', email=email, final_password=final_password, q1=q1, q2=q2,q3=q3)
    
    else:
        # Display the form with randomly selected questions
        three_questions = random.sample(list(sec_questions.items()), 3)
        q1 = three_questions[0][1]
        q2 = three_questions[1][1]
        q3 = three_questions[2][1]
    
        return render_template('password_generator.html', q1=q1, q2=q2,q3=q3)
    

if __name__ == '__main__':
    app.run(debug=True)
# =============================================
main()   
password_generator()

            



