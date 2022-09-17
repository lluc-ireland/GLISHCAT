import os
import csv
from pygame import mixer

class vocab_data:
    def __init__(self):
        mixer.init()
        self.category_dict = self.open_categories()
        self.text_dict = self.open_texts()
        self.vocab_dict = self.open_vocabulary()
        self.phrase_dict = self.open_phrases()


    def major_categories(self, lang):
        return self.map_categories(lang, list(filter(lambda row: float(row["id"]).is_integer(), self.category_dict)))

    def get_text(self, lang, id):
        row = next(filter(lambda row: row["id"] == id, self.text_dict))
        if lang == "en":
            return row["text_en"]
        else:
            return row["text_ca"]

    def get_vocabulary(self, lang, id):
        return self.map_texts(lang, list(filter(lambda row: float(row["id"]) == id, self.vocab_dict)), True, False)

    def get_sound_id(self, texttuple, cell_value):
        result = next(filter(lambda row: row[0].upper() == cell_value or row[1].upper() == cell_value, texttuple))
        if result[2].is_integer():
            return f"{int(result[2])}.{result[3]}"
        else:
            return f"{result[2]}.{result[3]}"

    def play_sound(self, sound_id, isphrase):
        path = os.path.join(os.path.dirname(__file__), (f"../data/sounds/phrases/{sound_id}.mp3" if isphrase else f"../data/sounds/vocabulary/{sound_id}.mp3"))
        if os.path.exists(path):
            mixer.music.load(path)
            mixer.music.play()

    def get_phrases(self, lang, id):
        return self.map_texts(lang, list(filter(lambda row: float(row["id"]) == id, self.phrase_dict)), True)

    def map_categories(self, lang, filter_list, ascending=True):
        if lang == "en":
            return sorted(list(map(lambda row: (row["text_en"], float(row["id"])), filter_list)), key=lambda tup: tup[0][0], reverse=ascending)   
        elif lang == "ca":
            return sorted(list(map(lambda row: (row["text_ca"], float(row["id"])), filter_list)), key=lambda tup: tup[0][0], reverse=ascending)
                        
    def map_texts(self, lang, filter_list, all=False, ascending=True):
        if lang == "en":
            if all == True:
                return sorted(list(map(lambda row: (row["text_en"], row["text_ca"], float(row["id"]), row["sound_id"]), filter_list)), key=lambda tup: tup[1][0], reverse=ascending)
            else:
                return sorted(list(map(lambda row: (row["text_en"], float(row["id"]), row["sound_id"]), filter_list)), key=lambda tup: tup[0][0], reverse=ascending)
        elif lang == "ca":
            if all == True:
                return sorted(list(map(lambda row: (row["text_ca"], row["text_en"], float(row["id"]), row["sound_id"]), filter_list)), key=lambda tup: tup[1][0], reverse=ascending)
            else:
                return sorted(list(map(lambda row: (row["text_ca"], float(row["id"]), row["sound_id"]), filter_list)), key=lambda tup: tup[0][0], reverse=ascending)

    def minor_categories(self, lang, id):
        return self.map_categories(lang, list(filter(lambda row: float(row["id"]) > id and float(row["id"]) < id + 1, self.category_dict)), False)

    def open_categories(self):
        with open(os.path.join(os.path.dirname(__file__), "../data/categories.txt"), "r") as file:
            return list(csv.DictReader(file))

    def open_texts(self):
        with open(os.path.join(os.path.dirname(__file__), "../data/texts.txt"), "r") as file:
            return list(csv.DictReader(file))

    def open_vocabulary(self):
        with open(os.path.join(os.path.dirname(__file__), "../data/vocabulary.txt"), "r") as file:
            return list(csv.DictReader(file))

    def open_phrases(self):
        with open(os.path.join(os.path.dirname(__file__), "../data/phrases.txt"), "r") as file:
            return list(csv.DictReader(file))
