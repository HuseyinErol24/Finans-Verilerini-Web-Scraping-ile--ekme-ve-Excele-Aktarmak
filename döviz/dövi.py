import requests
from colorama import Fore
from bs4 import BeautifulSoup
import pandas as pd

class DovizKuru():
    def __init__(self):
        link = "https://bigpara.hurriyet.com.tr/doviz/"
        self.baglanti = requests.get(link)
        self.exel_dizisi = []
        a = self.baglanti.status_code
        if a == 200:
            print(Fore.GREEN, end="")
            print("Bağlantı gerçekleştirildi....", Fore.WHITE)
            self.html_veri()
            self.exele_veri_yazmak()
        else:
            print(Fore.RED, end="")
            print("Bağlantı gerçekleştirilemedi....", Fore.WHITE)

    def html_veri(self):
        veri = self.baglanti.content
        html = BeautifulSoup(veri, "html.parser")
        self.kur = html.find("div", {"class": "contentLeft"}).find("div", {"class": "tableCnt"}).find("div", {
            "class": "tBody"}).find_all("ul")
        return self.kur

    def ayikla(self):
        dizi = []
        for i in self.kur:
            dizi1 = []
            h = str(i.text)
            h = h.split("\n")
            for m in range(1, 7):
                if m == 2:
                    continue
                else:
                    dizi1.append(h[m])
            dizi.append(dizi1)
        return dizi

    def exele_veri_yazmak(self):
        deger = self.ayikla()
        dizi = []

        for i in deger:
            alis = i[1]
            satis = i[2]
            fark = i[3]
            saat = i[4]
            dizi.append(alis)
            dizi.append(satis)
            dizi.append(fark)
            dizi.append(saat)
            self.exel_dizisi.append(dizi)
            dizi = []
        self.a = pd.DataFrame(self.exel_dizisi, columns=["Alis", "Satis", "Fark", "Saat"], index=[
            "ABD Doları",
            "Euro",
            "İngiliz Sterlini",
            "İsviçre Frangı",
            "Japon Yeni",
            "Suudi Arabistan Riyali",
            "Norveç Kronu",
            "Danimarka Kronu",
            "Avustralya Doları",
            "Kanada Doları",
            "İsveç Kronu",
            "Ruble",
        ])
        print(self.a)
        self.a.to_excel("Doviz_kurlari.xlsx", engine='openpyxl')

m = DovizKuru()
