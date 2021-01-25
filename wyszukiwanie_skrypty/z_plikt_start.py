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



#Dane do poszczególnych funkcji

#domowe.startFunction(y_start,m_start,d_start,y_stop,m_stop,d_stop)

#most_banned_champs_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

limit_champions = 200
most_picked_champs_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop,limit_champions)

#most_popular_role.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

#najlepsze_pary_graczchampion_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

#pick_and_banratio_dla_danego_champa_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

#win_ratios_OPT.startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop)

merge_all_to_a_book(glob.glob("*.csv"), "dane.xlsx")

