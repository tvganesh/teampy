from teamData import *
file="indiaTest.csv"
matchType="Test"
# Read CSV file
df = pd.read_csv(file)
# Clean data
df1 = cleanTeamData(df, matchType)

homeOrAway=["home"]

opposition="all"
# Get the vector of countries in opposition and filter those rows
if ("all" in  opposition):
   # Do not filter
   pass
else:
   df1 = df1[df1['Opposition'].isin(opposition)]


# Check home/away/neutral from vector homeOrAway and filter rows
if ("all"in homeOrAway ):
   # Do not filter
   pass

else:
   df1 = df1[df1['ha'].isin(homeOrAway)]


# Select columns, group and count
df1.groupby(['Opposition','ha','Result']).Opposition.agg('count').to_frame('count').reset_index()
