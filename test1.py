from teamData import *
import seaborn as sns 
import pandas as pd
file="indiaTest.csv"
matchType="Test"
# Read CSV file
df = pd.read_csv(file)
# Clean data
df1 = cleanTeamData(df, matchType)

homeOrAway=["all"]

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
#df2=df1.groupby(['Opposition','ha','Result']).Opposition.agg('count').to_frame('count').reset_index()
#sns.barplot(x="Result", y="count", data=df2, palette=sns.color_palette("GnBu", 10))
#df2=df1.groupby(['Opposition','ha',])['Result'].agg('count').to_frame('count').unstack(fill_value=0)

#df1.groupby(['Opposition','ha','Result']).Opposition.agg('count').to_frame('c')
#df2=df1.groupby(['Opposition','ha','Result']).Opposition.agg('count').to_frame('count').reset_index()
#status=sns.barplot(x="Opposition", y="count", hue=['ha'],data=df2)
#status.set_xticklabels(labels,rotation=30)
#status.set_xticklabels(status.get_xticklabels(), rotation=90)

# Works
df2=df1.groupby(['Opposition','Result','ha']).Opposition.agg('count').to_frame('count').unstack().fillna(0)['count']
df2.plot(kind='bar',stacked=False,legend=True,fontsize=8,width=1)



#Work1
#df2=df1.groupby(['Opposition','ha','Result']).Opposition.agg('count').to_frame('count').reset_index()
#status=sns.barplot(x="Opposition", y="count", hue='Result',data=df2)
#status.set_xticklabels(labels,rotation=30)
#status.set_xticklabels(status.get_xticklabels(), rotation=90)
