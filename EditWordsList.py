#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:51:52 2024

@author: tandyllc
"""
filtered_words = []
with open('words_alpha.txt', 'r') as input_file:
    words = input_file.readlines()

for line in words:
    # Process each word (remove newline characters and print)
    word = line.strip()  # Remove leading and trailing whitespace, including newline characters
    if len(word) <= 10 and len(word) >= 4:
        filtered_words.append(word)

# Open a new text file in write mode to store filtered words
with open('password_words.txt', 'w') as output_file:
    # Write each filtered word to the output file
    for word in filtered_words:
        output_file.write(word + '\n')