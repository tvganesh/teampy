import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 07 Jun 2019
# Function: getTeamNumber
# This function returns the team number for a team name for Tests, ODIs and T20s
#
###########################################################################################

def getTeamNumber(teamName,matchType):

   # Match type is Test
   if(matchType == "Test"):
     # Test teams
     teams = {"Afghanistan":40, "Australia":2,"Bangladesh":25,"England":1,"ICC World X1":40,
                 "India":6,"Ireland":29,"New Zealand":5,"Pakistan":7,"South Africa":3,
                 "Sri Lanka":8,"West Indies":4,"Zimbabwe":9}

   # Match type is ODI
   elif (matchType == "ODI"):
      # ODI teams
      teams = {"Afghanistan":40, "Africa XI":4058, "Asia XI":106, "Australia":2,
                 "Bangladesh":25,"Bermuda":12 ,"England":1,"ICC World X1":140,
                 "India":6,"Ireland":29,"New Zealand":5,"Pakistan":7,"South Africa":3,
                 "Sri Lanka":8,"West Indies":4,"Zimbabwe":9,"Canada":17,"East Africa":14,
                 "Hong Kong":19,"ICC World XI":140,"Ireland":29,"Kenya":26,"Namibia":28,
                 "Nepal":32,"Netherlands":15,"Oman":37,"Papua New Guinea":20,"Scotland":30,
                 "United Arab Emirates":27,"United States of America":11, "Zimbabwe":9}


   elif (matchType == "T20") :
       # T20 Teams
       teams = {"Afghanistan":40, "Australia":2,"Bahrain":108, "Bangladesh":25,
                 "Belgium":42, "Belize":115,"Bermuda":12,"Botswana" :116,"Canada":17,"Costa Rica":4082,
                 "Germany":35,"Ghana":135,"Guernsey":1094,"Hong Kong":19,"ICC World X1":140,
                 "India":6,"Ireland":29,"Italy":31, "Jersey":4083,"Kenya":26,"Kuwait":38,
                 "Maldives":164,"Malta":45,"Mexico":165,"Namibia":28,"Nepal":32,"Netherlands":15,
                 "New Zealand":5,"Nigeria":173, "Oman":37,"Pakistan":7,"Panama":183,"Papua New Guinea":20,
                 "Philippines":179,"Qatar":187,"Saudi Arabia":154,"Scotland":30,"South Africa":3,
                 "Spain":200, "Sri Lanka":8,"Uganda":34,"United Arab Emirates":27,
                 "United States of America":11,"Vanuatu":216,"West Indies":4}
   else :
       print("Unknown match ")
  
   # Return team number
   return(teams[teamName])

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 07 Jun 2019
# Function: getMatchType
# This function returns the match number for a  match type viz. Tests, ODIs and T20s
#
###########################################################################################

def getMatchType(matchType):
  match = {"Test":1,"ODI":2,"T20":3}
  return(match[matchType])
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 07 Jun 2019
# Function: getTeamData
# This function returns the team data as a CSV file and data frame for a given matchType
# homeOrAway and result vectors. This can be done for a given team as 'bat' or 'bowl'
# option
#
###########################################################################################
def getTeamData(teamName,dir=".",file="team001.csv",matchType="Test",
                        homeOrAway=[1,2,3],result=[1,2,3,4],teamView="bat",save=False) :

  # Initialize url to ""
  url =""
  suburl1 = "http://stats.espncricinfo.com/ci/engine/stats/index.html"

  # Get the match tyoe
  match =getMatchType(matchType)
  #Create suburl2
  suburl2 = "?class=" + str(match) + ";"

  suburl3 = "template=results;"
  suburl4 = "type=team;"
  suburl5 = "size=200;"
  suburl6 = "view=innings;"

  # Set the home or away depending on the values in homeOrAway vector
  str1=str2=str3=""
  if (1 in homeOrAway):
    str1 ="home_or_away=1;"
  
  if (2 in homeOrAway) :
    str2="home_or_away=2;"
  
  if (3 in  homeOrAway):
    str3="home_or_away=3;"
  
  HA = str1 + str2 + str3

  # Set the result based on  result vector
  str1=str2=str3=str4=""
  if(1 in result):
    str1 ="result=1;"

  if(2 in result):
    str2 ="result=2;"

  if (3 in result):
    str3 ="result=3;"
  

  # Test has result 'draw-4' while ODI and T20 have result 'no result-5'
  if(matchType == "Test"): #Test
    if(4 in result):
      str4 ="result=4;"

    else: #ODI & T20
      if(5 in result):
         str4 ="result=5;"
    
  
  result =str1+str2+str3+str4
  # Set the team

  # Get the team number
  team=getTeamNumber(teamName, matchType)

  # Set the team for which data is required
  theTeam= "team="+ str(team) +";"

  # Set the data view
  dataView ="team_view="+teamView+";"

  # Create composite URL
  baseurl = suburl1+suburl2+suburl3+suburl4+suburl5+suburl6+HA + result+theTeam+dataView
  print(baseurl)

  


  notDone = True
  i = 0
  teamDF = pd.DataFrame()
    
  # Loop through the data 200 (max)rows at a time
  while (notDone):
       i = i + 1
       page = ""
       page = "page=" + str(i)
       print(page)
       url = baseurl + page
       print(url)
       dfList= pd.read_html(url)
       df = dfList[2]
       print(df.shape)
        
       if(df.shape[0] == 1):
           break;
       else:
           teamDF= pd.concat([teamDF,df])
    
       if not os.path.exists(dir):
            os.mkdir(dir)
                # print("Directory " , dir ,  " Created ")
       else:
            pass
                # print("Directory " , dir ,  " already exists, writing to this folder")
        
       # Create path
       path = os.path.join(dir, file)
       
       print(teamDF.shape)
       if save:
            # Write to file 
            teamDF.to_csv(path)
   
  return(teamDF)


##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 07 Jun 2019
# Function: getTeamData
# This function returns the team data as a CSV file and data frame for a given matchType
# homeOrAway and result vectors along with a column which includes whether the match was
#home, away, neutral zone etc. This can be done for a given team as 'bat' or 'bowl'
# option
#
###########################################################################################

def getTeamDataHomeAway(teamName,dir=".",teamView="bat",matchType="Test",file="team001HA.csv",save=True):

  print("Working...")
  # Check if match type is Test. The result is won, lost, draw or tie
  if(matchType == "Test"):
    df1= getTeamData(teamName=teamName,dir=".",file="team001.csv",matchType=matchType,homeOrAway=[1],result=[1,2,3,4],teamView=teamView)
    df2= getTeamData(teamName=teamName,dir=".",file="team001.csv",matchType=matchType, homeOrAway=[2],result=[1,2,3,4],teamView=teamView)
    df3= getTeamData(teamName=teamName,dir=".",file="team001.csv",matchType=matchType, homeOrAway=[3],result=[1,2,3,4],teamView=teamView)
  else: #ODI & T20. The result is won, lost, tie or no result

    df1= getTeamData(teamName=teamName,dir=".",file="team001.csv",matchType=matchType,homeOrAway=[1],result=[1,2,3,5],teamView=teamView)
    df2= getTeamData(teamName=teamName,dir=".",file="team001.csv",matchType=matchType, homeOrAway=[2],result=[1,2,3,5],teamView=teamView)
    df3= getTeamData(teamName=teamName,dir=".",file="team001.csv",matchType=matchType, homeOrAway=[3],result=[1,2,3,5],teamView=teamView)
  
  print("hello")
  print(df1.shape)
  print(df2.shape)
  print(df3.shape)
  # Create the column values home, away or neutral
  df1['ha']="home"
  df2['ha']="away"
  df3['ha'] = "neutral"
  print("After")
  print(df1.shape)
  print(df2.shape)
  print(df3.shape)
  
  df = pd.DataFrame()
  
  # Stack the rows to create dataframe
  if(df1.shape[0] != 0):
      df = pd.concat([df,df1])
  if(df2.shape[0] != 0):
      df = pd.concat([df,df2])  
  if(df3.shape[0] != 0):
      df = pd.concat([df,df3])

  print("final",df.shape)   
  # Create path
  path = os.path.join(dir, file)
       
  if save:
    # Write to file 
      df.to_csv(path)
   
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 07 Jun 2019
# Function: cleanTeamData
# This function cleans the team data for Test, ODI and T20
#
###########################################################################################

def cleanTeamData(df,matchType):
  #Remove rows with 'DNB

  a=df.Score != 'DNB'
  df1 = df[a]
  
  if (matchType =="Test"):
    # Remove columns 0,8 & 12 for Tests. They have empty columns
    cols=[0,8,12]
    df2=df1.drop(df1.columns[cols],axis=1)
  # Remove columns 8 & 12 for ODI and T20. They have empty columns
  elif ((matchType == "ODI") or (matchType == "T20")):
    cols=[0,7,11]
    df2=df1.drop(df1.columns[cols],axis=1)
  

  # Fix the Opposition column, remove "^ v"
  df2.Opposition=df2.Opposition.str.replace("v ","")
  # Return cleaned dataframe
  return(df2)

      
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 07 Jun 2019
# Function: teamWinLossStatusVsOpposition
# This function returns a team's win/loss/draw/tie status against the opposition. The
# matches could be played at home/away/neutral venues for Test, ODI and T20
#
###########################################################################################

def teamWinLossStatusVsOpposition(file,teamName,opposition=["all"],homeOrAway=["all"],matchType="Test",plot=False):

  # Read CSV file
  df = pd.read_csv(file)
  print(df.columns)
  # Clean data
  df1 = cleanTeamData(df, matchType)
  print(df1.columns)

 
  # Get the list of countries in opposition and filter those rows
  if ("all" in  opposition):
    # Do not filter
    pass
  else:
    df1 = df1[df1['Opposition'].isin(opposition)]
  
  print(df1.columns)
  # Check home/away/neutral from list homeOrAway and filter rows
  if ("all"in homeOrAway ):
     # Do not filter
     pass 
  else:
    df1 = df1[df1['ha'].isin(homeOrAway)]
  

  # Select columns, group and count
  df2=df1.groupby(['Opposition','ha','Result']).Opposition.\
         agg('count').to_frame('count')
  print(df2.columns)

  # If plot is True
  if(plot == True):
    # Collapse list of countries in opposition
    separator='-'
    oppn = separator.join(opposition)
    # Collapse vectors of homeOrAway vector
    ground = separator.join(homeOrAway)

    atitle = "Win/Loss status of " + teamName +  " against opposition in " +  matchType +"(s)"

    asub ="Against " + oppn + " teams at " +  ground +  " grounds"

    df3 = df2.reset_index()
    # Plot for opposition and home/away for a team in Tes, ODI and T20
    status=sns.barplot(x="Opposition", y="count", hue='Result',data=df3)

    status.set_xticklabels(status.get_xticklabels(), rotation=90)
    
    plt.xlabel('Opposition')
    plt.ylabel('Win/Loss count')
    plt.suptitle(atitle)
    plt.title(asub)
  else:
    # Return dataframe
    return(df2)

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 07 Jun 2019
# Function: teamWinLossStatusAtGrounds
# This function returns a team's win/loss/draw/tie status against the opposition at venues.
# The matches could be played at home/away/neutral venues for Test, ODI and T20s. The output is either a
# dataframe or a plot
#
###########################################################################################

def teamWinLossStatusAtGrounds(file,teamName,opposition=["all"],homeOrAway=["all"],matchType="Test",plot=False):
  # Read CSV file
  df = pd.read_csv(file)
  # Clean data
  df1 = cleanTeamData(df, matchType)

 
  # Get the list of countries in opposition and filter those rows
  if ("all" in  opposition):
    # Do not filter
    pass
  else:
    df1 = df1[df1['Opposition'].isin(opposition)]
  
  print(df1.columns)
  # Check home/away/neutral from list homeOrAway and filter rows
  if ("all"in homeOrAway ):
     # Do not filter
     pass 
  else:
    df1 = df1[df1['ha'].isin(homeOrAway)]
  

  # Select columns, group and count
  df2=df1.groupby(['Ground','ha','Result']).Opposition.\
         agg('count').to_frame('count')
  print(df2.columns)

  # If plot is True
  if(plot == True):
    # Collapse list of countries in opposition
    separator='-'
    oppn = separator.join(opposition)
    # Collapse vectors of homeOrAway vector
    ground = separator.join(homeOrAway)

    atitle = "Win/Loss status of " + teamName +  " against opposition in " +  matchType +"(s)"

    asub ="Against " + oppn + " teams at " +  ground +  " grounds"

    df3 = df2.reset_index()
    # Plot for opposition and home/away for a team in Tes, ODI and T20
    status=sns.barplot(x="Ground", y="count", hue='Result',data=df3)
    status.set_xticklabels(status.get_xticklabels(), rotation=90)
    plt.xlabel('Ground')
    plt.ylabel('Win/Loss count')
    plt.suptitle(atitle)
    plt.title(asub)
  else:
    # Return dataframe
    return(df2)
    
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 07 Jun 2019
# Function: plotTimelineofWinsLosses
# This function plot the timelines of win/lost/draw/tie against opposition at
# venues for Test, ODI and T20s
#
###########################################################################################

def plotTimelineofWinsLosses(file,teamName,opposition=["all"],homeOrAway=["all"],
                                     startDate="2001-01-01",endDate="2019-01-01",matchType="Test"):
    
    # Read CSV file
    df = pd.read_csv(file)
    # Clean data
    df1 = cleanTeamData(df, matchType)
  
    # Get the list of countries in opposition and filter those rows
    if ("all" in opposition):
        # Do not filter
        pass
    else:
        df1 = df1[df1['Opposition'].isin(opposition)]
    
    print(df1.columns)
    # Check home/away/neutral from list homeOrAway and filter rows
    if ("all" in homeOrAway):
        # Do not filter
        pass
    else:
        df1 = df1[df1['ha'].isin(homeOrAway)]
    
    # FIlter won and set to 1
    a = df1.Result == "won"
    df2 = df1[a]
    if (df2.shape[0] != 0):
        df2['result'] = 1
    
    # Filter tie and set to 0.5
    a = df1.Result == "tie"
    df3 = df1[a]
    # No tie
    if (df3.shape[0] != 0):
        df3['result'] = 0.5
    
    # Test has w
    if (matchType == "Test"):
        # FIlter draw and set to -0.5
        a = df1.Result == "draw"
        df4 = df1[a]
        if (df4.shape[0] != 0):  # No draw
            df4['result'] = 0
    elif ((matchType == "ODI") or (matchType == "T20")):
        # FIlter 'no result' and set to 0
        a = df1.Result == "n/r"
        df4 = df1[a]
        if (df4.shape[0] != 0):
            df4['result'] = -0.5
    
    # Filter lost and set to -1
    a = df1.Result == "lost"
    df5 = df1[a]
    if (df5.shape[0] != 0):
        df5['result'] = -1
    
    df6 = pd.concat([df2, df3, df4, df5])
    print(df6.shape)
    df6['date'] = pd.to_datetime(df6['Start Date'])
    separator = '-'
    oppn = separator.join(opposition)
    # Collapse vectors of homeOrAway vector
    ground = separator.join(homeOrAway)
    
    atitle = "Timeline of Win/Loss status of " + teamName + " in " + matchType + "(s)"
    asub = "Against " + oppn + " teams at " + ground + " grounds"
    
    # Sort by Start date
    df7 = df6[['date', 'result']].sort_values(by='date')
    print(df7.head())
    # Filter between start and end dates
    m = ((df7.date >= startDate) & (df7.date <= endDate))
    df8 = df7[m]
    
    if (matchType == "Test"):
        plt.plot(df8['date'], df8['result'])
        plt.axhline(y=1, color='r')
        plt.axhline(y=0.5, color='b')
        plt.axhline(y=0, color='y')
        plt.axhline(y=-1, color='y')
        plt.xlabel('Date')
        plt.ylabel('Win/Loss status')
        plt.suptitle(atitle)
        plt.title(asub)
    
    
    elif ((matchType == "ODI") or (matchType == "T20")):
        plt.plot(df8['date'], df8['Result'])
        plt.axhline(y=1, color='r')
        plt.axhline(y=0.5, color='b')
        plt.axhline(y=-0.5, color='y')
        plt.axhline(y=-1, color='y')
        plt.xlabel('Date')
        plt.ylabel('Win/Loss status')
        plt.suptitle(atitle)
        plt.title(asub)
    
#getTeamDataHomeAway(teamName="Bangladesh",save=True)
#getTeamDataHomeAway(teamName="India",matchType="Test",file="indiaTest.csv",save=True)
#df1= getTeamData(dir=".",file="team001.csv",matchType="Test",homeOrAway=[1],result=[1,2,3,4],teamName="Bangladesh")
#df=pd.read_csv("indiaTest.csv")
#df1=cleanTeamData(df,matchType="Test")

#df=teamWinLossStatusVsOpposition("indiaTest.csv",teamName="India",opposition=["all"],homeOrAway=["all"],matchType="Test",plot=False)
#teamWinLossStatusVsOpposition("indiaTest.csv",teamName="India",opposition=["all"],homeOrAway=["all"],matchType="Test",plot=True)
#teamWinLossStatusAtGrounds("indiaTest.csv",teamName="India",opposition=["Australia"],homeOrAway=["home"],matchType="Test",plot=True)
#getTeamDataHomeAway(teamName="South Africa",matchType="T20",file="southafricaT20.csv",save=True)
  
#plotTimelineofWinsLosses("indiaTest.csv",teamName="India")
teamWinLossStatusVsOpposition("southafricaT20.csv",teamName="South Africa",opposition=["all"],homeOrAway=["all"],matchType="T20",plot=True)