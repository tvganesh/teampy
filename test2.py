file="indiatest.csv"
# Read CSV file
df = pd.read_csv(file)
# Clean data
df1 = cleanTeamData(df, matchType)

opposition=["all"]
homeOrAway=["all"]
teamName="India"
startDate="2001-01-01"
endDate="2019-01-01"
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
elif ((matchType == "ODI") or (matchType == "T20")):
    plt.plot(df8['date'], df8['Result'])