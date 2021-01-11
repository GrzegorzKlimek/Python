from arango import ArangoClient
import csv

# Ustawienia zakresu
y_start = 2020
m_start = 11
d_start = 10
y_stop = 2020
m_stop = 11
d_stop = 30

client = ArangoClient(hosts='http://k53.pietryga.info:8529')
db = client.db('Riot', username='adam', password='moraipraktyki321')
# Execute an AQL query and iterate through the result cursor.
query_str = """
let date_start = DATE_TIMESTAMP(@year_start, @month_start, @day_start) // Czy to mam gdzieś zwrócić / wypisać?
let date_stop = DATE_TIMESTAMP(@year_stop, @month_stop, @day_stop)

//let a = (
//        FOR z IN Match2
//            FILTER  u.gameCreation >= date_start  and
//              u.gameCreation <= date_stop  
//              COLLECT server = z.server WITH COUNT INTO games
//              Return games
//    )

FOR u IN Match2

//LIMIT @LIMIT          Ograniczenie ilosci zapytan
    FILTER  u.gameCreation >= date_start  and
            u.gameCreation <= date_stop

    COLLECT server = u.server 
    AGGREGATE gameDuration = AVERAGE (u.gameDuration)
//  WITH COUNT INTO games
    RETURN{
    "server" : server,
    "avgGameDuration" : CONCAT(
            FLOOR(gameDuration/60),
            " m ",
            ROUND(gameDuration - FLOOR(gameDuration/60) * 60),
            " s"),
//   "count" : a[0] 
    }

"""

# Ustawienie czasu/rankingu na jakim

cursor = db.aql.execute(query_str, bind_vars={'year_start': y_start,
                                              'month_start': m_start, 'day_start': d_start, 'year_stop': y_stop,
                                              'month_stop': m_stop,
                                              'day_stop': d_stop})
match_servers = [document for document in cursor]

# Możemy ustawić dokladniejsza nazwe pliku jeśli istnieje taka potrzeba

with open('zadanie1' + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['server', 'avgGameDuration', 'from', 'to']
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwriter.writeheader()
    start = str(y_start) + '.' + str(m_start) + '.' + str(d_start)
    end = str(y_stop) + '.' + str(m_stop) + '.' + str(
        d_stop)
    opis = {'from': start, 'to': end}
    csvwriter.writerow(opis)

    for match in match_servers:
        csvwriter.writerow(match)

#      print(match)


