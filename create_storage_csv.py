#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 22:28:23 2024

@author: tandyllc
"""
import pandas as pd

def create_password_csv():
    password_table = [
        'User Email',
        'Index of password associated with this email',
        'Generated Password',
        'Date',
        'What is the name of your childhood best friend?',
        'In which city did your parents meet?',
        'What was your first car brand?',
        'What is a nickname you had at home?',
        'What is the name of your first pet?',
        'What is the maiden name of your grandmother?',
        'What is the first concert you attended?'
        'What was the name of your 7th grade history teacher?',
        'What is your favorite film you saw in theaters?'
        ]
    
    dataframe_template = pd.DataFrame(columns=password_table)
    
    dataframe_template.to_csv('password_user_data.csv', index=False)
    
create_password_csv()