import sqlite3 as sqli
import re
from azureapi import azurettsapi
import os
class respce:
    def __init__(self, pert, rep):
        self.pert = pert
        self.rep = rep

conn = sqli.connect("bnQuran.db")

cur = conn.cursor()
wrong = []
wrong.append(respce(r"([ ])(পার)([ ,।;])", r"\1পারো\3"))
wrong.append(respce(r"([ ])(কর)([ ,।;])", r"\1করো\3"))
wrong.append(respce(r"\ ব্যতীত\ ", " ব্যতীতো "))
wrong.append(respce(r"([^্])(য)", r"\1জ"))
# যাননা বিশদ
res = cur.execute("Select surah_id, verse_id, bn_bayan from quran where surah_id=2 and verse_id=255")
output = open("quranout.log", "w", encoding="utf-8")
for data in res.fetchall():
    filename = "audio/bn_bayan-"+str(data[0])+"."+str(data[1])+".mp3"
    if not os.path.isfile(filename):
        text = data[2]
        # currection of produnce
        for currection in wrong:
            text = re.sub(currection.pert, currection.rep,text)
        azurettsapi(text, filename)
output.close()