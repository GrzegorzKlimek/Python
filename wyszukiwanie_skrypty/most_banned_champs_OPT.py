from arango import ArangoClient
import csv


def startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop):

    client = ArangoClient(hosts='http://k53.pietryga.info:8529')
    db = client.db('Riot', username='adam', password='moraipraktyki321')
    # Execute an AQL query and iterate through the result cursor.
    query_str = """
    /*
    5 najczęściej  wybieranych championów we wrześniu dla dywizji GrandMaster i Challenger na EUW. 
    
    */
    
    // Join LeagueEntry oraz Alias w celue wskazania interesujących aliasów
    let players = (for la in LeagueEntry
        filter   la.legueKey == concat(@LEAGUE, '\@', @server)
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
    let r = range(firstDay, endDay)
    
    
    for m in Match2
        //LIMIT @LIMIT
        filter m.dayFromStart in firstDay..endDay
        filter m.server == @server
        filter m.queueId == 420 or  m.queueId == 700
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
        
        let bans = APPEND(m.teams[0].bans , m.teams[1].bans)
        
        
        
        FOR ban in bans
           COLLECT  bannedChampionId =  ban.championId WITH COUNT INTO freq
            SORT freq desc
            RETURN {
             "banned champion" : Document("Champion", TO_STRING(bannedChampionId)).name ,
             "count" : freq
            }
    """
    cursor = db.aql.execute(query_str, bind_vars={'LEAGUE': rank, 'server': server, 'year_start': y_start,
                                                  'month_start': m_start, 'day_start': d_start, 'year_stop': y_stop,
                                                  'month_stop': m_stop, 'day_stop': d_stop})
    match_servers = [document for document in cursor]

    with open('most_banned_champs_OPT_'+ server + '_' + rank + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['banned champion', 'count', 'from', 'to', 'server', 'league']
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
#      print(match)


