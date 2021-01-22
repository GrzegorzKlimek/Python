from arango import ArangoClient
import csv


def startFunction(rank,server,y_start,m_start,d_start,y_stop,m_stop,d_stop):

    client = ArangoClient(hosts='http://k53.pietryga.info:8529')
    db = client.db('Riot', username='adam', password='moraipraktyki321')
    # Execute an AQL query and iterate through the result cursor.
    query_str = """
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
    let r = range(firstDay, endDay)
    
    
    For m in Match2
            
            filter m.dayFromStart in r
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
            //LIMIT @LIMIT
            LET t0w = m.teams[0].win == 'Win'
            COLLECT AGGREGATE 
            fBloodWins =     sum( t0w ? (m.teams[0].firstBlood  ? 1 : 0) : (m.teams[1].firstBlood  ? 1 : 0)),
            fTowerWins =     sum( t0w ? (m.teams[0].firstTower  ? 1 : 0) : (m.teams[1].firstTower  ? 1 : 0)),
            fInhibitoWins =   sum( t0w ? (m.teams[0].firstInhibitor  ? 1 : 0) : (m.teams[1].firstInhibitor  ? 1 : 0)),
            fRiftHeraldWins = sum( t0w ? (m.teams[0].firstRiftHerald  ? 1 : 0) : (m.teams[1].firstRiftHerald  ? 1 : 0)),
            fDragonWins =    sum( t0w ? (m.teams[0].firstDragon  ? 1 : 0) : (m.teams[1].firstDragon  ? 1 : 0)),
            fBaronWins =      sum( t0w ? (m.teams[0].firstBaron  ? 1 : 0) : (m.teams[1].firstBaron  ? 1 : 0)),
            games =           sum(1),
            gamesRift = sum((m.teams[0].firstRiftHerald or m.teams[1].firstRiftHerald) ? 1 :0 ),
             gamesDragon = sum((m.teams[0].firstDragon or m.teams[1].firstDragon) ? 1 :0 ),
              gamesBaron = sum((m.teams[0].firstBaron or m.teams[1].firstBaron) ? 1 :0 )
            
    let fBloodWinRate = fBloodWins/games
    let fTowerWinsRate = fTowerWins/games
    let fInhibitoWinsRate = fInhibitoWins/games
    let fRiftHeraldWinsRate = fRiftHeraldWins/gamesRift
    let fDragonWinsRate = fDragonWins/gamesDragon
    let fBaronWinRatesRate = fBaronWins/gamesBaron
    
    RETURN {
        "Number of matches": games,
        "First blood win rate" : fBloodWinRate,
        "First Tower win rate" : fTowerWinsRate,
        "First Inhibitor win rate" : fInhibitoWinsRate,
        "First Rift Hearld win rate" : fRiftHeraldWinsRate,
        "First Dragon kill win rate" : fDragonWinsRate,
        "First Baron kill win rate" : fBaronWinRatesRate,
    }
    """
    cursor = db.aql.execute(query_str, bind_vars={'LEAGUE': rank, 'server': server,'year_start': y_start,
                                                  'month_start': m_start, 'day_start': d_start, 'year_stop': y_stop, 'month_stop': m_stop, 'day_stop': d_stop})
    match_servers = [document for document in cursor]

    with open('win_ratios_OPT_' + server + '_' + rank + '.csv', 'w', encoding='utf-8', newline='') as csvfile:

        fieldnames = ['Number of matches', 'First blood win rate', 'First Tower win rate', 'First Inhibitor win rate', 'First Rift Hearld win rate', 'First Dragon kill win rate', 'First Baron kill win rate', 'from', 'to', 'server', 'league']
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


