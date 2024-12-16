#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 10:35:30 2024

@author: cjohnson
"""

import tkinter as tk
from tkinter.filedialog import askopenfilenames

root = tk.Tk()
root.withdraw()
root.lift()

filenames = askopenfilenames()
root.update()
root.destroy()

print(filenames)
