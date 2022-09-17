from faulthandler import enable
import tkinter as tk
import vocab_data as vd
from tkinter import ttk
from tkinter import messagebox as msg
from functools import partial

data = vd.vocab_data()
lang = "ca"

class vocab_categories(tk.Toplevel):
    def __init__(self, master, id):
        super().__init__()
        self.geometry("1600x600")
        self.title("GLISHCAT")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.config(background="#765D69")

        self.category_frame = ttk.Frame(self, width=150)
        self.vocab_frame = ttk.Frame(self)
        self.buttons = []

        vocab = data.get_text(lang, "vocabulary")
        phrases = data.get_text(lang, "phrases")
        minor_cat = data.minor_categories(lang, id)

        v_lang1 = f"{vocab} Català" if lang == "ca" else f"English {vocab}"
        v_lang2 = f"{vocab} Anglès" if lang == "ca" else f"Catalan {vocab}"
        p_lang1 = f"{phrases} Català" if lang == "ca" else f"English {phrases}"
        p_lang2 = f"{phrases} Anglès" if lang == "ca" else f"Catalan {phrases}"

        self.tree = ttk.Treeview(self.vocab_frame, columns=(
            "vocabulary1", "vocabulary2", "phrases1", "phrases2"), show="headings")
        self.tree.heading("vocabulary1", text=f"{v_lang1}")
        self.tree.heading("phrases1", text=f"{p_lang1}")
        self.tree.heading("vocabulary2", text=f"{v_lang2}")
        self.tree.heading("phrases2", text=f"{p_lang2}")

        self.tree.column("vocabulary1", anchor="center")
        self.tree.column("phrases1", anchor="center")
        self.tree.column("vocabulary2", anchor="center")
        self.tree.column("phrases2", anchor="center")
        self.tree.tag_configure('gray', background='#cccccc')

        self.tree.pack(fill=tk.BOTH, expand=1)
        self.category_frame.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        self.vocab_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        if len(minor_cat) > 0:
            for ca in minor_cat:
                button = ttk.Button(self.category_frame, text=ca[0].capitalize(
                ), command=partial(self.cat_button, ca[1]))
                self.buttons.append((button, ca[1]))
                button.pack(side=tk.TOP, fill=tk.X)
        else:
            self.cat_button(id)

    def selectItem(self, vocab, phrase, event):
        curItem = self.tree.item(self.tree.focus())
        col = self.tree.identify_column(event.x)
        sound_id = "0"

        if col == '#1':
            cell_value = curItem['values'][0]
            sound_id = data.get_sound_id(vocab, cell_value) 
        elif col == '#2':
            cell_value = curItem['values'][1]
            sound_id = data.get_sound_id(vocab, cell_value) 
        elif col == '#3':
            cell_value = curItem['values'][2]
            sound_id = data.get_sound_id(phrase, cell_value) 
        elif col == '#4':
            cell_value = curItem['values'][3]
            sound_id = data.get_sound_id(phrase, cell_value) 

        if lang == "ca":
            if col == '#2' or col == '#4':
                data.play_sound(sound_id, col == '#4')
        else:
            if col == '#1' or col == '#3':
                data.play_sound(sound_id, col == '#3')      

    def cat_button(self, id):
        for item in self.tree.get_children():
            self.tree.delete(item)

        vocab = data.get_vocabulary(lang, id)
        phrase = data.get_phrases(lang, id)

        self.tree.bind('<ButtonRelease-1>', partial(self.selectItem, vocab, phrase))

        flag = False

        if len(vocab) >= len(phrase):
            for t, voc in enumerate(vocab):
                flag = True if flag == False else False
                if t < len(phrase):
                    self.tree.insert("", tk.END, values=(
                        voc[1].upper(), voc[0].upper(), phrase[t][1].upper(), phrase[t][0].upper()), tag='gray' if flag == True else '')
                else:
                    self.tree.insert("", tk.END, values=(
                        voc[1].upper(), voc[0].upper(), "", ""), tag='gray' if flag == True else '')
        else:
            for t, phr in enumerate(phrase):
                flag = True if flag == False else False
                if t < len(vocab):
                    self.tree.insert("", tk.END, values=(
                        vocab[t][1].upper(), vocab[t][0].upper(), phr[1].upper(), phr[0].upper()), tag='gray' if flag == True else '')
                else:
                    self.tree.insert("", tk.END, values=(
                        "", "", phr[1].upper(), phr[0].upper()), tag='gray' if flag == True else '')

        for but in self.buttons:
            but[0].configure(style="TButton")

        but = next(filter(lambda b: b[1] == id, self.buttons))
        but[0].configure(style="H.TButton")

    def on_close(self):
        for but in self.master.buttons:
            but[0].configure(style="TButton")
        self.destroy()

class vocab_ui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x600")
        self.title("GLISHCAT")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#F1828D",
                        foreground="#FEFAD4", font=(None, 24), anchor="center")
        style.configure("TButton", background="#F1828D",
                        foreground="#FEFAD4", font=(None, 16), anchor="center")
        style.configure("Treeview", background="#FEFAD4", foreground="#F1828D")
        style.configure("Treeview.Heading", background="#F1828D",
                        foreground="#FEFAD4", font=(None, 16), anchor="center")
        style.configure("TFrame", background="#765D69")
        style.configure("H.TButton", foreground="#F1828D",
                        background="#FEFAD4")
        style.configure("EN.TButton", foreground="#8FB9A8",
                        background="#FEFAD4")

        def fixed_map(option):
            # Fix for setting text colour for Tkinter 8.6.9
            # From: https://core.tcl.tk/tk/info/509cafafae
            #
            # Returns the style map for 'option' with any styles starting with
            # ('!disabled', '!selected', ...) filtered out.

            # style.map() returns an empty list for missing options, so this
            # should be future-safe.
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]  

        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
                              

        self.main_frame = ttk.Frame(self)

        self.welcome_label = ttk.Label(
            self.main_frame, text=data.get_text("ca", "welcome"))
        self.welcome_label.pack(side=tk.TOP, fill=tk.X)

        self.toggle_btn = ttk.Button(
            self.main_frame, text="ca->en", width=12, command=self.toggle)
        self.toggle_btn.pack(side=tk.TOP, pady=5)
        self.buttons = []

        for ca in data.major_categories(lang):
            button = ttk.Button(self.main_frame, text=ca[0].capitalize(
            ), command=partial(self.cat_button, ca[1]))
            self.buttons.append((button, ca[1]))
            button.pack(side=tk.BOTTOM, fill=tk.X)

        self.main_frame.pack(fill=tk.BOTH, expand=1)

    def cat_button(self, id):
        for but in self.buttons:
            but[0].configure(style="TButton")

        but = next(filter(lambda b: b[1] == id, self.buttons))
        but[0].configure(style="H.TButton")

        vocab_categories(self, id)

    def toggle(self):
        global lang
        if lang == "en":
            self.toggle_btn.configure(text="ca->en", style="TButton")
            for ca, lab in zip(data.major_categories("ca"), self.buttons):
                lab[0].configure(text=ca[0].capitalize(),
                                 command=partial(self.cat_button, ca[1]))
            self.welcome_label.configure(text=data.get_text("ca", "welcome"))
            lang = "ca"
        else:
            self.toggle_btn.configure(text="en->ca", style="EN.TButton")
            for en, lab in zip(data.major_categories("en"), self.buttons):
                lab[0].configure(text=en[0].capitalize(),
                                 command=partial(self.cat_button, en[1]))
            self.welcome_label.configure(text=data.get_text("en", "welcome"))
            lang = "en"


if __name__ == "__main__":
    root = vocab_ui()
    root.mainloop()
