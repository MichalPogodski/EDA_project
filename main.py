import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

df = pd.DataFrame()

def read_data():
    global df
    directory = 'names'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # print(filename[3:7])
            df1 = pd.DataFrame(pd.read_csv(str(directory) + '/' + filename, delimiter=',', names=['name', 'sex', 'number']))
            df1['year'] = int(filename[3:7])
            df = pd.concat([df, df1])
        else:
            continue

    df.sort_values("year", axis=0, inplace=True, ascending=True)
    df.reset_index(drop=True, inplace=True)
    print(df)


def task_2():
    table_temp = df.nunique(axis=0)
    print('liczba unikalnych imion: ', table_temp['name'])


def task_3():
    table_temp = df.groupby('sex').nunique()
    print('liczba unikalnych imion zenskich: ', table_temp['name']['F'])
    print('liczba unikalnych imion meskich: ', table_temp['name']['M'])


def task_4():
    global df
    df_dividend = df.groupby(['year', 'sex', 'name']).sum()
    # print("df_temp: \n", df_dividend)

    df_divisor = df_dividend.groupby(['year', 'sex']).sum()
    # print("df_temp2: \n", df_divisor)

    freq = df_dividend.div(df_divisor)
    # print("freq: \n", freq)

    res = df.join(freq, ['year', 'sex', 'name'], rsuffix='2')
    res.rename(columns={"number2": "frequency_male"}, inplace=True)
    res['frequency_female'] = res['frequency_male']
    res.loc[res['sex'] == 'F', "frequency_male"] = 0
    res.loc[res['sex'] == 'M', "frequency_female"] = 0
    df = res
    print(df)




if __name__ == '__main__':
    read_data()
    # task_2()
    # task_3()
    task_4()



