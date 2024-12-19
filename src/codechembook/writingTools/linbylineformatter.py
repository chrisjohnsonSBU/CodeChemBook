# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 14:29:39 2024

@author: benle
"""
import re




def generate_linebyline(file, output = "latex")
'''
This function parses a file that has both code and comments that are meant as line-by-line comments.
The code breaks the file into two new files: 
    - one that is just the python code 
    - one that is the line-by-line comments
    
The formatting of this source file is as follows:
    - all line-by-line comments start with r"""# # where the two numbers are the indentation level (starting at 0) and the number of lines of code the comment block covers. 
    - If the comment is meant to cover a range of code, then the second number should be preceded by an &
    - Within a comment block, adding an indentation level is indicated by adding a + and reducing the indentation level is indicated by -
    - within a comment block, a new line comment is indicated by !, followed by the number of lines past the first one that it applies to
    
'''

# open up the file, and read each line, generating two lists: one that will have each line for the code, and one that will have the formatted line-by-line comments.
code = []
comments = []
indent_amount = "3" # in units of em
codeline = 0
current_indent_level = 0
with open(file, "r") as f:
    mode = "code"
    for i, line in ennumerate(f):
        if line[0:5]: # this is a comment block
            mode = "comment"
            comment_indent_level = # first number
            n_comment_lines = # the second number is the number of lines 
            for n_indents in range(comment_indent_level - current indent level,0,-1):
                comments.append("\begin{itemize}")
                
                
                
#%%
for r in range(-1, 0 , -1):
    print(r)