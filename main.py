# -*- coding: utf-8 -*-
"""
Created on Fri May  6 11:58:00 2022

@author: ngomi
"""

from detector import detector as dt

import tkinter as tk
from tkinter import filedialog, Text
import os


root = tk.Tk()

detector = dt()
detector.beginDetec()

root.mainloop()

