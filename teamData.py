import pandas as pd
import os
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
    df1= getTeamData(teamView,teamName=teamName,dir=".",file="team001.csv",matchType=matchType,homeOrAway=[1],result=[1,2,3,4])
    df2= getTeamData(teamView,teamName=teamName,dir=".",file="team001.csv",matchType=matchType, homeOrAway=[2],result=[1,2,3,4])
    df3= getTeamData(teamView,teamName=teamName,dir=".",file="team001.csv",matchType=matchType, homeOrAway=[3],result=[1,2,3,4])
  else: #ODI & T20. The result is won, lost, tie or no result

    df1= getTeamData(teamView,teamName=teamName,dir=".",file="team001.csv",matchType=matchType,homeOrAway=[1],result=[1,2,3,5])
    df2= getTeamData(teamView,teamName=teamName,dir=".",file="team001.csv",matchType=matchType, homeOrAway=[2],result=[1,2,3,5])
    df3= getTeamData(teamView,teamName=teamName,dir=".",file="team001.csv",matchType=matchType, homeOrAway=[3],result=[1,2,3,5])
  
  # Create the column values home, away or neutral
  df1.ha="home"
  df2.ha="away"
  df3.ha = "neutral"

  # Stack the rows to create dataframe
  print(df1.shape)
  print(df2.shape)
  print(df3.shape)

#getTeamData(teamName="Bangladesh",save=True)
df1= getTeamData(dir=".",file="team001.csv",matchType=matchType,homeOrAway=[1],result=[1,2,3,4],teamName="Bangladesh")