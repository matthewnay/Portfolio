import unicodedata

import pandas as pd
from unidecode import unidecode

import numpy as np

total = 0
dfbattingmaster = None
for year in ['2015', '2016', '2017',  '2018', '2019', '2021', '2022']:

    df = pd.read_csv(f'battingvalue{year}.csv')

    df = df[['Name', 'Age', 'Tm', 'G', 'PA', 'WAR', 'Salary', 'Pos Summary', 'Name-additional']]

    df.dropna(inplace=True)


    df = df[df['Pos Summary'] != '1']
    df = df[df['PA'] >= 502]
    df['Year'] = int(year)
    df['Salary'] = df['Salary'].str.replace(',', '').str.replace('$','').astype(float)

    # print(df.dtypes)
    # print(df.head())
    # print(df.shape)
    total += df.shape[0]
    # print(df.describe())

    # df.to_csv(f'battingvalue{year}(v2).csv', index=False)
    dfbattingmaster = pd.concat ([dfbattingmaster, df], axis=0)

# dfbattingmaster.to_csv('battingvaluemaster.csv', index=False)

total2 = 0
dfpitchingmaster = None
for year in ['2015', '2016', '2017',  '2018', '2019', '2021', '2022']:

    df = pd.read_csv(f'pitchingvalue{year}.csv')

    df = df[['Name', 'Age', 'Tm', 'G', 'IP', 'WAR', 'Salary', 'Name-additional']]

    df.dropna(inplace=True)


    df = df[df['IP'] >= 162]
    df['Year'] = int(year)
    df['Salary'] = df['Salary'].str.replace(',', '').str.replace('$','').astype(float)

    # print(df.dtypes)
    # print(df.head())
    # print(df.shape)
    total2 += df.shape[0]
    # print(df.describe())

    # df.to_csv(f'pitchingvalue{year}(v2).csv', index=False)
    dfpitchingmaster = pd.concat([dfpitchingmaster, df], axis=0)

# dfpitchingmaster.to_csv('pitchingvaluemaster.csv', index=False)

# print(total, total2)
# print(total+total2)

battingstats = pd.read_csv('battingstats.csv')
# print(battingstats.head())
# print(battingstats.columns)
battingstats['Name'] = battingstats['first_name'] + ' ' + battingstats['last_name']
# print(battingstats.head())

# def clean_name(name):
#     # Convert name to uppercase and remove non-alphanumeric characters
#     return ''.join(e for e in name.upper() if e.isalnum())

def clean_name(name):
    if not pd.isna(name):
        name = unicodedata.normalize('NFD', str(name)).encode('ascii', 'ignore').decode('ascii')
        return ''.join(e for e in name.upper() if e.isalnum())
    else:
        return None


dfbattingmaster['Name'] = dfbattingmaster['Name'].apply(unidecode)
dfbattingmaster['Name'] = dfbattingmaster['Name'].apply(clean_name)
battingstats['Name'] = battingstats['Name'].apply(unidecode)
battingstats['Name'] = battingstats['Name'].apply(clean_name)

battingstats['Year'] = battingstats['year']

battingmaster = pd.merge(dfbattingmaster, battingstats, how='left', on=['Name', 'Year'])


# print(battingmaster.dtypes)
# print(battingmaster.head())
# print(battingmaster.shape)
# print(battingmaster.describe())

# battingmaster.to_csv('battingmaster.csv', index=False)



######### adding birth stats ############
demosheet = pd.read_csv('retrosheet.csv')
demosheet['Name'] = demosheet['NICKNAME'] + ' ' + demosheet['LAST']
# print(demosheet.head())


demosheet = demosheet[['Name', 'BIRTHDATE', 'BIRTH CITY', 'BIRTH STATE', 'BIRTH COUNTRY', 'PLAY DEBUT']]
# print(demosheet.dtypes)
# demosheet.to_csv('demosheet.csv', index=False)
demosheet.dropna(inplace=True)
demosheet['Name'] = demosheet['Name'].apply(unidecode)
demosheet['Name'] = demosheet['Name'].apply(clean_name)
# print(demosheet.head())

battingmaster = pd.merge(battingmaster, demosheet, how='left', on='Name')

# battingmaster.to_csv('battingmaster(1).csv', index=False)

battingmaster['debut'] = pd.to_datetime(battingmaster['PLAY DEBUT'])
battingmaster['Year'] = pd.to_datetime(battingmaster['year'], format='%Y').dt.year

battingmaster['ServiceTime'] = battingmaster['Year'] - pd.DatetimeIndex(battingmaster['debut']).year

# print(battingmaster.shape)
battingmaster.dropna(inplace=True)
# print(battingmaster.shape)
# print(battingmaster['ServiceTime'].value_counts())
# print(battingmaster.dtypes)

# outliers = battingmaster[battingmaster['ServiceTime'] == 0]
# outliers.to_csv('outliers.csv', index=False)
battingmaster = battingmaster[battingmaster['Salary'] >= 1000000]
# print(battingmaster['ServiceTime'].value_counts())
print(battingmaster.shape)

# battingmaster.to_csv('battingmaster.csv', index=False)

#### pitching ####
pitchingstats = pd.read_csv('pitchingstats.csv')
pitchingstats['Name'] = pitchingstats['first_name'] + ' ' + pitchingstats['last_name']
dfpitchingmaster['Name'] = dfpitchingmaster['Name'].apply(unidecode)
dfpitchingmaster['Name'] = dfpitchingmaster['Name'].apply(clean_name)
pitchingstats['Name'] = pitchingstats['Name'].apply(unidecode)
pitchingstats['Name'] = pitchingstats['Name'].apply(clean_name)

pitchingstats['Year'] = pitchingstats['year']

# print(pitchingstats.head())

pitchingmaster = pd.merge(dfpitchingmaster, pitchingstats, how='left', on=['Name', 'Year'])

# pitchingmaster.to_csv('pitchingmaster.csv', index=False)

pitchingmaster = pd.merge(pitchingmaster, demosheet, how='left', on='Name')



pitchingmaster['debut'] = pd.to_datetime(pitchingmaster['PLAY DEBUT'])
pitchingmaster['Year'] = pd.to_datetime(pitchingmaster['year'], format='%Y').dt.year

pitchingmaster['ServiceTime'] = pitchingmaster['Year'] - pd.DatetimeIndex(pitchingmaster['debut']).year


# print(pitchingmaster.shape)
pitchingmaster.dropna(inplace=True)
# print(pitchingmaster.shape)
# print(pitchingmaster['ServiceTime'].value_counts())
# print(pitchingmaster.dtypes)
#
# # outliers = battingmaster[battingmaster['ServiceTime'] == 0]
# # outliers.to_csv('outliers.csv', index=False)
pitchingmaster = pitchingmaster[pitchingmaster['Salary'] >= 1000000]
# print(pitchingmaster['ServiceTime'].value_counts())
print(pitchingmaster.shape)
#
print(battingmaster.shape[0]+pitchingmaster.shape[0])

# pitchingmaster.to_csv('pitchingmaster.csv', index=False)


battingfull = pd.read_csv('battingmasterfull.csv')

print(battingfull['BIRTH COUNTRY'].value_counts())

pitchingfull = pd.read_csv('pitchingmasterfull.csv')

print(pitchingfull['BIRTH COUNTRY'].value_counts())

battingfull['International'] = battingfull['BIRTH COUNTRY'] != 'USA'
pitchingfull['International'] = pitchingfull['BIRTH COUNTRY'] != 'USA'

print(battingfull[['BIRTH COUNTRY', 'International']].head())

print(battingfull['Tm'].value_counts())

battingfull['ln_Salary'] = np.log(battingfull['Salary'])
pitchingfull['ln_Salary'] = np.log(pitchingfull['Salary'])


battingfull.to_csv('battingmaster.csv', index=False)
#
# pitchingfull.to_csv('pitchingmaster.csv', index=False)

