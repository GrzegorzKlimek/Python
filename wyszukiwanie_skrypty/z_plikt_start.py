import domowe
import most_picked_champs_OPT
import most_banned_champs_OPT
import most_popular_role
import pick_and_banratio_dla_danego_champa_OPT
import najlepsze_pary_graczchampion_OPT
import win_ratios_OPT
import glob
import json
from pyexcel.cookbook import merge_all_to_a_book

#Dane ogólne
rank = 'challenger'
server = 'euw1'
y_start = 2020
m_start = 11
d_start = 29
y_stop = 2020
m_stop = 11
d_stop = 30

list_champions = {
1: "Annie",
2: "Olaf",
3: "Galio",
4: "TwistedFate",
5: "XinZhao",
6: "Urgot",
7: "Leblanc",
8: "Vladimir",
9: "Fiddlesticks",
10: "Kayle",
11: "MasterYi",
12: "Alistar",
13: "Ryze",
14: "Sion",
15: "Sivir",
16: "Soraka",
17: "Teemo",
18: "Tristana",
19: "Warwick",
20: "Nunu",
21: "MissFortune",
22: "Ashe",
23: "Tryndamere",
24: "Jax",
25: "Morgana",
26: "Zilean",
27: "Singed",
28: "Evelynn",
29: "Twitch",
30: "Karthus",
31: "Chogath",
32: "Amumu",
33: "Rammus",
34: "Anivia",
35: "Shaco",
36: "DrMundo",
37: "Sona",
38: "Kassadin",
39: "Irelia",
40: "Janna",
41: "Gangplank",
42: "Corki",
43: "Karma",
44: "Taric",
45: "Veigar",
48: "Trundle",
50: "Swain",
51: "Caitlyn",
53: "Blitzcrank",
54: "Malphite",
55: "Katarina",
56: "Nocturne",
57: "Maokai",
58: "Renekton",
59: "JarvanIV",
60: "Elise",
61: "Orianna",
62: "MonkeyKing",
63: "Brand",
64: "LeeSin",
67: "Vayne",
68: "Rumble",
69: "Cassiopeia",
72: "Skarner",
74: "Heimerdinger",
75: "Nasus",
76: "Nidalee",
77: "Udyr",
78: "Poppy",
79: "Gragas",
80: "Pantheon",
81: "Ezreal",
82: "Mordekaiser",
83: "Yorick",
84: "Akali",
85: "Kennen",
86: "Garen",
89: "Leona",
90: "Malzahar",
91: "Talon",
92: "Riven",
96: "KogMaw",
98: "Shen",
99: "Lux",
101: "Xerath",
102: "Shyvana",
103: "Ahri",
104: "Graves",
105: "Fizz",
106: "Volibear",
107: "Rengar",
110: "Varus",
111: "Nautilus",
112: "Viktor",
113: "Sejuani",
114: "Fiora",
115: "Ziggs",
117: "Lulu",
119: "Draven",
120: "Hecarim",
121: "Khazix",
122: "Darius",
126: "Jayce",
127: "Lissandra",
131: "Diana",
133: "Quinn",
134: "Syndra",
136: "AurelionSol",
141: "Kayn",
142: "Zoe",
143: "Zyra",
145: "Kaisa",
147: "Seraphine",
150: "Gnar",
154: "Zac",
157: "Yasuo",
161: "Velkoz",
163: "Taliyah",
164: "Camille",
201: "Braum",
202: "Jhin",
203: "Kindred",
222: "Jinx",
223: "TahmKench",
235: "Senna",
236: "Lucian",
238: "Zed",
240: "Kled",
245: "Ekko",
246: "Qiyana",
254: "Vi",
266: "Aatrox",
267: "Nami",
268: "Azir",
350: "Yuumi",
360: "Samira",
412: "Thresh",
420: "Illaoi",
421: "RekSai",
427: "Ivern",
429: "Kalista",
432: "Bard",
497: "Rakan",
498: "Xayah",
516: "Ornn",
517: "Sylas",
518: "Neeko",
523: "Aphelios",
526: "Rell",
555: "Pyke",
777: "Yone",
875: "Sett",
876: "Lillia"
}

#Dane do poszczególnych funkcji

#domowe.startFunction(y_start,m_start,d_start,y_stop,m_stop,d_stop)

#most_banned_champs_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

limit_champions = 200
most_picked_champs_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop,limit_champions,list_champions)

#most_popular_role.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

#najlepsze_pary_graczchampion_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

#pick_and_banratio_dla_danego_champa_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

#win_ratios_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

merge_all_to_a_book(glob.glob("*.csv"), "dane.xlsx")

