from arango import ArangoClient
import csv


def startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop):

    client = ArangoClient(hosts='http://k53.pietryga.info:8529')
    db = client.db('Riot', username='adam', password='moraipraktyki321')

    query_str = """
    /* 2.
     Most popular role in challenger Przykładowo w challengerze w Korei mamy 200 graczy, dla każdego z nich określamy na
    jakiej roli gra najczęściej i pokazujemy jaki to jest rozkład( np. Mid 56, jgl 42, bot 38, Supp
    35, Top 29). Lub w ujęciu procentowym. Należy określić jaka minimalna liczba gier w
    Challengerze w danym okresie kwalifikuje gracza do udziału w statystyce. Należy sprawdzić
    w danych z api czy widzimy wszystkie 5 ról (widać)
    */
    
    // Join LeagueEntry oraz Alias w celue wskazania interesujących aliasów
    let players = (for la in LeagueEntry
        filter la.legueKey == concat(@LEAGUE, '\@', @server)
        for a in Alias
            filter a.origin == la._key
            collect aliases = [a._key, a.origin]
            
    return aliases)
    
    let aliasTab =  ( for p in players return p[0] )
    let idTab    =  ( for p in players return p[1] )
    let aliasDict = zip(aliasTab, idTab)
    
    
    
    // Ustalanie zakresu dat jako liczby dni od początku 2015
    let startTimestamp = DATE_TIMESTAMP(@year_start, @month_start, @day_start)
    let firstDay = (DATE_YEAR(startTimestamp)-2015) * 366 + DATE_DAYOFYEAR(startTimestamp)
    let endTimestamp = DATE_TIMESTAMP(@year_stop, @month_stop, @day_stop)
    let endDay = (DATE_YEAR(endTimestamp)-2015) * 366 + DATE_DAYOFYEAR(endTimestamp)
    //let r = range(firstDay, endDay)
    
    //
    for m in Match2
       // LIMIT @LIMIT
        filter m.dayFromStart in firstDay..endDay
        filter m.server == @server
        filter m.queueId == 420 or  m.queueId == 700
       
        // selekcja interesujących graczy
        let goodAliases = [
            aliasDict[m.aliases[1]],
            aliasDict[m.aliases[2]],
            aliasDict[m.aliases[3]],
            aliasDict[m.aliases[4]],
            aliasDict[m.aliases[5]],
            aliasDict[m.aliases[6]],
            aliasDict[m.aliases[7]],
            aliasDict[m.aliases[8]],
            aliasDict[m.aliases[9]],
            aliasDict[m.aliases[10]]
        ]
        
        FILTER COUNT_DISTINCT(goodAliases) > 1
        //COLLECT WITH COUNT INTO games
        //RETURN games
        
        let timelines = m.timelines
    
        for i in range(0, 9)
          filter goodAliases[i] != null
            let tl = timelines[i+1]
            let game = 1
            let r_duo = tl.role == "DUO"
            let r_duo_carry = tl.role == "DUO_CARRY"
            let r_duo_support = tl.role == "DUO_SUPPORT"
            let r_none = tl.role == "NONE"
            let r_solo = tl.role == "SOLO"
            
            let l_bot = tl.lane == "BOTTOM"
            let l_mid = tl.lane == "MIDDLE"
            let l_none = tl.lane == "NONE"
            let l_top = tl.lane == "TOP"
            let l_jungle = tl.lane == "JUNGLE"
            
                
            let b_bot = r_duo_carry or ( l_bot and (r_duo or r_solo))
            let b_mid = l_mid and (r_duo or r_solo)
            let b_support = r_duo_support or (r_duo and l_none)
            let b_jungle = l_jungle or (r_none and l_none)
            let b_top = l_top and (r_duo or r_solo)
            
            
    
            let support = b_support ? 1 : 0
            let mid = b_mid  ? 1 : 0
            let jungle = b_jungle ? 1 : 0
            let top = b_top ? 1 : 0
            let bot = b_bot ? 1 : 0
        
            collect user = Document("LeagueEntry", goodAliases[i]).summonerName
            aggregate bots = Sum(bot),
                      mids = Sum(mid),
                      jungles = Sum(jungle),
                      tops = Sum(top),
                      supports = Sum(support),
                      games = sum(game)
            
            
    
    filter games > 1
    sort games desc
    return 
          { "user": user, 
           "games": games, 
           "bot": bots,
           "mid": mids,
           "top": tops,
           "jungle": jungles,
           "support": supports,
          }
         
    """
    cursor = db.aql.execute(query_str, bind_vars={'LEAGUE': rank, 'server': server, 'year_start': y_start,
                                                  'month_start': m_start, 'day_start': d_start, 'year_stop': y_stop,
                                                  'month_stop': m_stop, 'day_stop': d_stop})
    match_servers = [document for document in cursor]

    with open('most_popular_role_' + server + '_' + rank + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['user', 'games', 'bot', 'mid', 'top', 'jungle', 'support', 'from', 'to', 'server', 'league']

        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        start = str(y_start) + '.' + str(m_start) + '.' + str(d_start)
        end = str(y_stop) + '.' + str(m_stop) + '.' + str(
            d_stop)
        opis = {'from': start, 'to': end, 'server': server, 'league': rank}
        csvwriter.writerow(opis)

        for match in match_servers:
            csvwriter.writerow(match)
    return 0


