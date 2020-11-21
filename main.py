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
    # df.to_csv("task_4.csv")


def task_5():
    df_temp_num = df.groupby(['year']).sum()
    print("df_temp_num: \n", df_temp_num)
    df_temp_sex_num = df.groupby(['sex', 'year']).sum()
    # print("df_temp_sex_num: \n", df_temp_sex_num)

    df_temp_num['div'] = df_temp_sex_num['number']['F'] / df_temp_sex_num['number']['M']
    male_max = max(df_temp_sex_num['number']['M'])
    print(male_max)
    ax = df_temp_num.plot(kind='line', subplots=True)
    plt.show()
#########################################################wyczysc wykres + maksy (dokoncz polecenie)################


def task_6():
    df_temp = df.groupby(['year', 'sex', 'name']).sum()
    df_temp.sort_values("number", axis=0, inplace=True, ascending=False)
    df_temp = df_temp.head(1000)
    print('df_temp: \n', df_temp)
    df_top = df_temp.groupby(['sex', 'name']).sum()
    df_top.sort_values("number", axis=0, inplace=True, ascending=False)
    print('df_top: \n', df_top)

def task_7():
    

if __name__ == '__main__':
    read_data()
    # task_2()
    # task_3()
    # task_4()
    # task_5()   #########################################################wyczysc wykres + maksy (dokoncz polecenie)################
    # task_6()
    task_7()

