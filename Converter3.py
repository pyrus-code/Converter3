import tkinter
import tkinter as tk
import tkinter.messagebox
from collections import deque
from string import digits
from tkinter import Menu, IntVar, StringVar
from tkinter import font
import re

converter_window = tk.Tk()
converter_window.title("Converter")
converter_window.configure(background="white")
converter_window.geometry("400x400")

def com_exit():
    askyesno = tkinter.messagebox.askyesno("Converter", "Do you want to exit?")
    com_exit = askyesno
    if com_exit>0:
        converter_window.destroy()
        return

def com_eraseall():
    com_eraseall = tkinter.messagebox.askyesno("Erase All", "Do You want erase all data?")
    if com_eraseall>0:
        Value_entry.delete(0, tkinter.END)
        lbl_result['text'] = "The Result"
        return

user_preferences_decimal = {"conversion_type": 1, "decimals": 1}


def digits_validation(digits):
    digits = Value_entry.get()
    pattern = r'^\d+(\.\d+)?$'
    return bool(re.match(pattern, digits))


def convert_value(input_value):
    decimals = user_preferences_decimal["decimals"]
    if user_preferences_decimal["conversion_type"] == 1:
        converted = input_value / 1.609
        label = "{:.{d}f} Km = {:.{d}f} Miles".format(input_value, converted, d=decimals)
        Value_entry.delete(0, tkinter.END)
    else:
        converted = input_value * 1.609
        label = "{:.{d}f} Miles = {:.{d}f} Km".format(input_value, converted, d=decimals)
        Value_entry.delete(0, tkinter.END)
    return converted, label.format(converted)

decimals = user_preferences_decimal["decimals"]

cache_results = deque(maxlen=5)

open_windows = {"options": None,"history": None}

def com_convert():
    if not digits_validation(digits):
        tkinter.messagebox.showerror("Error", "Please, introduce only numbers")
    else:
        Km_data = float(Value_entry.get())
        result, formatted_result = convert_value(Km_data)
        lbl_result.config(text=formatted_result)
        conversion_type = "Km to Miles" if user_preferences_decimal["conversion_type"] == 1 else "Miles to Km"
        cache_results.append((Km_data, result, conversion_type))
        return

class validation(tk.Entry):
    def __init__(self,master,max_length, **kwargs):
        super().__init__(master, **kwargs)
        self.max_length = max_length
        text_max_checker = converter_window.register(self.is_valid_length)
        self.configure(validate="key", validatecommand=(text_max_checker, "%P"))

    def is_valid_length(self, text):
        if self.max_length:
            if len(text) > self.max_length:
                return False
        return True

def open_moreoptions():
    if open_windows["history"] and open_windows["history"].winfo_exists():
        open_windows["history"].destroy()
        open_windows["history"] = None

    if open_windows["options"] is None or not open_windows["options"].winfo_exists():
        open_windows["options"] = moreoptions()
    else:
        open_windows["options"].lift()

def open_history():
    if open_windows["options"] and open_windows["options"].winfo_exists():
        open_windows["options"].destroy()
        open_windows["options"] = None

    if open_windows["history"] is None or not open_windows["history"].winfo_exists():
        open_windows["history"] = historycache(cache_results)
    else:
        open_windows["history"].lift()


class moreoptions(tk.Toplevel):

    def __init__(self,*args, callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.grab_set()
        self.temp_cache = {}
        self.moreoptions()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def moreoptions(self):
        self.title("More Options")
        self.geometry("300x250")

        self.moreoptions_title = tk.Label(self, text="More Options", font=("Garamond", 20, font.BOLD))
        self.moreoptions_title.grid(row=1,padx=30, pady=5)

        self.optionsvar = IntVar()
        self.optionsvar.set(1)
        self.kmtomiles = tk.Radiobutton(self, text="Km to Miles",variable=self.optionsvar, value=1)
        self.kmtomiles.grid(row=2,padx=30, pady=5)
        self.milestokm = tk.Radiobutton(self, text="Miles to KM", variable=self.optionsvar, value=2)
        self.milestokm.grid(row=3,padx=30, pady=5)

        self.options_decimal_list = ["1","2","3"]
        self.lst_menu = StringVar(self)
        self.lst_menu.set("1")

        self.lst_menu_label = tk.Label(self, text="Decimal caracteres")
        self.lst_menu_label.grid(row=4, column=0, padx=40, pady=5, columnspan=1, sticky="w")
        self.lst_decimalcombo = tk.OptionMenu(self, self.lst_menu, *self.options_decimal_list)
        self.lst_decimalcombo.grid(row=4,column=0,padx=145, pady=5, columnspan=2)
        self.btn_saveoptions = tk.Button(self,text="Save",height=2, width=8,font=("Garamond", 10, font.BOLD),command=self.save_moreoptions)
        self.btn_saveoptions.grid(row=5,padx=30,pady=5)

    def save_moreoptions(self):
        conversion_type = self.optionsvar.get()
        decimals = self.lst_menu.get()
        user_preferences_decimal["conversion_type"] = conversion_type
        user_preferences_decimal["decimals"] = int(decimals)

        open_windows["options"] = None
        self.destroy()

    def on_close(self):
        open_windows["options"] = None
        self.destroy()

class historycache(tk.Toplevel):

    def __init__(self,cache_results, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.grab_set()
        self.cache_results = cache_results
        self.historycache()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def historycache(self):
        self.title("Previous Results")
        self.geometry("400x300")

        self.lbl_cache = tk.Label(self, text="", font=("Garamond", 16, "bold"), justify="left")
        self.lbl_cache.grid()
        self.historycache_results()

        self.btn_exit = tk.Button(self, text="Exit", height=2, width=10, font=("Garamond", 10, "bold"),command=self.destroy)
        self.btn_exit.grid(row=5,padx=30,pady=5)

    def historycache_results(self):
        self.history_text = "\n".join([f"{conversion_type}: {original:.{user_preferences_decimal['decimals']}f} → {result:.{user_preferences_decimal['decimals']}f}"
            for original, result, conversion_type in reversed(cache_results)])
        self.lbl_cache.config(text=self.history_text)

    def on_close(self):
        open_windows["history"] = None
        self.destroy()


menubar = Menu()
filemenu= Menu(menubar, tearoff=0)
menubar.add_cascade(label ="File", menu=filemenu)
filemenu.add_command(label="Erase All", command=com_eraseall)
filemenu.add_command(label="Exit", command=com_exit)


title_label= tk.Label (master=converter_window, text="Converter Km to Miles", background="white", font=("Garamond", 26, font.BOLD))
title_label.grid(row=1,column=1,padx=30, pady=10)

Value_entry = validation(master=converter_window, max_length=15,highlightbackground="grey",highlightthickness=2, width=20,font=("Garamond", 15, font.BOLD))
Value_entry.grid(row=2,column=1,padx=30, pady=10)

btn_convert = tk.Button(master=converter_window, text="Convert", height=2, width=15, font=("Garamond", 10, font.BOLD), command=com_convert)
btn_convert.grid(row=3,column=1,padx=30, pady=30)

lbl_result =tk.Label (master=converter_window, text="The Result", font=("Garamond", 24,font.BOLD), bg="yellow")
lbl_result.grid(row=4,column=1,padx=30, pady=10)

btn_history = tk.Button(master=converter_window, text="Previous Results", height=2, width=12, font=("Garamond", 10, font.BOLD), command=lambda: open_history())
btn_history.grid(row=5,column=1,padx=30, pady=1, columnspan=1, sticky="w")

btn_options = tk.Button(master=converter_window, text="More Options", height=2, width=12, font=("Garamond", 10, font.BOLD), command=lambda: open_moreoptions())
btn_options.grid(row=5,column=0, padx=30, pady=30, columnspan=2, sticky="s")

converter_window.configure(menu=menubar)
converter_window.mainloop()