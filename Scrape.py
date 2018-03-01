import urllib3
import certifi
from bs4 import BeautifulSoup
import pandas as pd



def SearchTeamAbbreviations():
        Eastern = ['TOR','FLA','MTL','CBJ','BUF',
                   'PHI','WSH','NJD','OTT','NYR',
                   'NYI','TBL','PIT','CAR','DET',
                   'BOS']
        Western = ['COL','VAN','EDM','LAK','CGY',
                   'ARI','MIN','NSH','WPG','SJS',
                   'VEG','DAL','ANA','STL','CHI']


#def CalculateGameAdvancedStats(team_df,goalie_df):
    #Calculate the Corsi, Fenwick, etc





            
def LoadGameStats(url="https://www.hockey-reference.com/boxscores/201710090BUF.html"):

    def findBasicHeaders(sp,starting_point=0):
    #Could be variable number of 'tr' entries prior to the table we want.
    # Find the one that contains 'Goals' (not 'Rk' because Goalies have that too)
        candidates = sp.findAll('tr')
        for i in range(starting_point,100):
            column_headers = [th.getText() for th in candidates[i].findAll('th')]
            try:
                if column_headers[2] == "G":
                    return i
            except:
                pass

    def findGoalieHeaders(sp,starting_point=0):
        #Search for the Goalie tables
        candidates = sp.findAll('tr')
        for i in range(starting_point,100):
            column_headers = [th.getText() for th in candidates[i].findAll('th')]
            try:
                if column_headers[2] == "DEC":
                    return i
            except:
                pass

    def findAdvancedHeaders(sp,starting_point=0):
    #Could be variable number of 'tr' entries prior to the table we want.
    # Find the one that contains 'Goals' (not 'Rk' because Goalies have that too)
        candidates = sp.findAll('tr')
        for i in range(starting_point,100):
            column_headers = [th.getText() for th in candidates[i].findAll('th')]
            print(column_headers)
            try:
                if column_headers[1] == "iCF":
                    return i
            except:
                pass

    

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    r = http.request('GET', url).data
    soup = BeautifulSoup(r,'lxml')
            
    header = findBasicHeaders(soup)
    column_headers = [th.getText() for th in soup.findAll('tr',limit=header+1)[header].findAll('th')]

    #Get the away team info
    data_rows = soup.findAll('tr')[header:header+20]
    
    player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                for i in range(len(data_rows))]
    
    away_df = pd.DataFrame(player_data[2:],columns=column_headers[1:])


    
    #And home team
    header2 = findBasicHeaders(soup,header+1)
    data_rows = soup.findAll('tr')[header2:header2+20]
    
    player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                for i in range(len(data_rows))]

    home_df = pd.DataFrame(player_data[2:],columns=column_headers[1:])
#    print(home_df.head)

    #Away goalie
    header3 = findGoalieHeaders(soup)
    column_headers = [th.getText() for th in soup.findAll('tr',limit=header3+1)[header3].findAll('th')]
    
    data_rows = soup.findAll('tr')[header3:header3+2]
    
    player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                for i in range(len(data_rows))]
    
    away_goalie_df = pd.DataFrame(player_data[1:],columns=column_headers[1:])
#    print(away_goalie_df.head)
    
    #Home goalie
    header4 = findGoalieHeaders(soup,header3+1)
    column_headers = [th.getText() for th in soup.findAll('tr',limit=header4+1)[header4].findAll('th')]
    
    data_rows = soup.findAll('tr')[header4:header4+2]

    player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                for i in range(len(data_rows))]
    
    home_goalie_df = pd.DataFrame(player_data[1:],columns=column_headers[1:])
#    print(home_goalie_df.head)

#Get the away team advanced stats
#TODO: Somehow this is hidden in comments on the page
    header5 = findAdvancedHeaders(soup,header4+1)
    column_headers = [th.getText() for th in soup.findAll('tr',limit=header5+1)[header].findAll('th')]
    data_rows = soup.findAll('tr')[header5:header5+20]
    player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                for i in range(len(data_rows))]
    away_adv_df = pd.DataFrame(player_data[2:],columns=column_headers[1:])
    print(away_adv_df)



LoadGameStats()
