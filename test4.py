import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
plot=True
matchType="Test"
file="indiatest.csv"
# Read CSV file
df = pd.read_csv(file)
# Clean data
df1 = cleanTeamData(df, matchType)

opposition=["all"]
homeOrAway=["all"]
teamName="India"
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

# Select columns, group and count
df2 = df1.groupby(['Ground', 'ha', 'Result']).Opposition. \
    agg('count').to_frame('count')
print(df2.columns)

# If plot is True
if (plot == True):
    print("Here111")
    # Collapse list of countries in opposition
    separator = '-'
    oppn = separator.join(opposition)
    # Collapse vectors of homeOrAway vector
    ground = separator.join(homeOrAway)

    atitle = "Win/Loss status of " + teamName + " against opposition in " + matchType + "(s)"

    asub = "Against " + oppn + " teams at " + ground + " grounds"

    df3 = df2.reset_index()
    # Plot for opposition and home/away for a team in Tes, ODI and T20
    status = sns.barplot(x="Ground", y="count", hue='Result', data=df3, ci=None)
    status.set_xticklabels(status.get_xticklabels(), rotation=90)
    plt.xlabel('Ground')
    plt.ylabel('Win/Loss count')
    plt.suptitle(atitle)
    plt.title(asub)
    plt.text(5, 10, 'Data source-Courtesy:http://cricsheet.org',
             horizontalalignment='center',
             verticalalignment='center',
             )
else:
    # Return dataframe
    print(df2.head())