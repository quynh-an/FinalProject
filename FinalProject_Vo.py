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
    elif password_type == "2":
        password_min = input("Enter the minimum number of characters you need for your password: ")
        password_max = input("Enter the maximum number of characters you want for your password: ")
        break
    else:
        print("Invalid option. Please select 1 or 2.")
        
password_length = random(password_min, password_max)