import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sqlite3

df = pd.DataFrame()
df2 = pd.DataFrame()

def task_1():
    print('ZADANIE 1:')
    global df
    directory = 'names'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            df1 = pd.DataFrame(pd.read_csv(str(directory) + '/' + filename, delimiter=',', names=['name', 'sex', 'number']))
            df1['year'] = int(filename[3:7])
            df = pd.concat([df, df1])
        else:
            continue

    df.sort_values("year", axis=0, inplace=True, ascending=True)
    df.reset_index(drop=True, inplace=True)
    print(df, '\n')



def task_2():
    print('ZADANIE 2:')
    table_temp = df.nunique(axis=0)
    print('liczba unikalnych imion: ', table_temp['name'], '\n')



def task_3():
    print('ZADANIE 3:')
    table_temp = df.groupby('sex').nunique()
    print('liczba unikalnych imion zenskich: ', table_temp['name']['F'])
    print('liczba unikalnych imion meskich: ', table_temp['name']['M'], '\n')



def task_4():
    print('ZADANIE 4:')
    global df
    df_dividend = df.groupby(['year', 'sex', 'name']).sum()
    df_divisor = df_dividend.groupby(['year', 'sex']).sum()
    freq = df_dividend.div(df_divisor)

    res = df.join(freq, ['year', 'sex', 'name'], rsuffix='2')
    res.rename(columns={"number2": "frequency_male"}, inplace=True)
    res['frequency_female'] = res['frequency_male']
    res.loc[res['sex'] == 'F', "frequency_male"] = 0
    res.loc[res['sex'] == 'M', "frequency_female"] = 0
    df = res
    print(df, '\n')



def task_5():
    print('ZADANIE 5:')
    df_temp_num = df.groupby(['year']).sum()
    df_temp_sex_num = df.groupby(['sex', 'year']).sum()
    df_temp_num['div'] = df_temp_sex_num['number']['F'] / df_temp_sex_num['number']['M']

    print('Najwieksza roznice w liczbie urodzen miedzy chlopcami a dziewczynkami  zanotowano w ',
          df_temp_num.sort_values('div', ascending=False).head(1).index.values[0],
          'roku. Najmniejsza w ',
          df_temp_num.sort_values('div', ascending=True).head(1).index.values[0],
          'roku. \n')

    rename_dict = {'number': 'number of births', 'div': 'sex factor in births'}
    df_temp_num.rename(columns=rename_dict, inplace=True)

    df_res = df_temp_num[['number of births', 'sex factor in births']]
    ax = df_res.plot(kind='line', subplots=True, title='ZADANIE 5')



def task_6():
    print('ZADANIE 6:')
    df_temp = df.sort_values(['sex', 'number'], ascending=[False, False])
    df_res = df_temp.groupby(['year', 'sex']).head(1000)

    df_res1 = df_res.groupby(['sex', 'name']).sum()
    df_res2 = df_res1.sort_values(['sex', 'number'], ascending=[False, False])
    df_top = df_res2.groupby('sex').head(1000)
    del df_top['year']

    print(df_top)

    df_8 = pd.merge(df_temp, df_top, how='inner', on=['name'])
    del df_8['number_y']
    df_8.rename(columns={'number_x': 'number'}, inplace=True)
    return df_8



def task_7():#uzupelnij Marilin , danePobierzZPoprzedniegoAleDodajKOmentarzDoWywolania
    print('ZADANIE 7: wykres')
    df_temp = df.groupby(['name', 'year']).sum()
    fig, ax0 = plt.subplots()
    ax1 = ax0.twinx()

    ax0.set_ylabel('number (lines)')
    ax1.set_ylabel('popularity (dots)')
    fig.suptitle('ZADANIE 7')

    df_temp['number']['Harry'].plot(ax=ax0, color='tab:red', label='Harry')
    df_temp['number']['Marilin'].plot(ax=ax0, color='tab:purple', label='Marilin')
    df_temp['number']['James'].plot(ax=ax0, color='tab:blue', label='James')
    df_temp['number']['Mary'].plot(ax=ax0, color='tab:green', label='Mary')
    ax0.legend()

    df_temp2 = df.groupby(['sex', 'year']).sum()
    fam1 = df_temp['number']['Harry'] / df_temp2['number']['M']
    fam1.plot(ax=ax1, color='tab:red', marker='o')
    fam2 = df_temp['number']['Marilin'] / df_temp2['number']['F']
    fam2.plot(ax=ax1, color='tab:purple', marker='o')
    fam3 = df_temp['number']['James'] / df_temp2['number']['M']
    fam3.plot(ax=ax1, color='tab:blue', marker='o')
    fam4 = df_temp['number']['Mary'] / df_temp2['number']['F']
    fam4.plot(ax=ax1, color='tab:green', marker='o')



def task_8(top1000):
    print('ZADANIE 8: wykres')
    all_names = df.groupby(['year', 'sex']).nunique()
    del all_names['number']
    top_names = top1000.groupby(['year', 'sex']).nunique()
    del top_names['number']

    df_merged = pd.merge(all_names, top_names, how='inner', on=['year', 'sex'])
    df_merged['top / all'] = df_merged['name_y'] / df_merged['name_x'] * 100

    df_res = pd.pivot_table(df_merged, values='top / all', columns='sex', index='year', aggfunc=np.sum)
    ax = df_res.plot(title='ZADANIE 8')
    ax.set_ylabel('procentowy udział imion z rankingu top1000')
    ax.set_xlabel('lata')
    ax.legend(["Kobiety", "Mezczyzni"])

    df_res['diff'] = abs(df_res['M'] - df_res['F'])
    print('Najwieksza roznice w roznorodnosci pomiedzy imionami zenskimi a meskimi zanotowano w ',
          df_res.sort_values('diff', ascending=False).head(1).index.values[0], 'roku.')



def task_9():
    print('ZADANIE 9: wykres')
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.suptitle('ZADANIE 9')
    df_temp = df
    last_letter = list(df_temp['name'])
    for i, elem in enumerate(last_letter): last_letter[i] = elem[-1]
    df_temp['last_letter'] = last_letter
    df_backup = df_temp.groupby(['last_letter', 'year']).sum()
    df_temp = df_temp.groupby(['last_letter', 'year', 'sex']).sum()
    df_temp = df_temp.loc[:, [1910, 1960, 2015], :]
    df_divisor = df.groupby('year').sum()
    df_temp['number'] /= df_divisor['number']
    df_temp = df_temp.loc[:, :, 'M']
    df_res = pd.pivot_table(df_temp, values='number', index='last_letter',
                    columns='year', aggfunc=np.sum)

    ax = df_res.plot.bar(ax=axes[0])

    df_res['diff'] = abs(df_res[1910] - df_res[2015])
    df_res.sort_values(['diff'], inplace=True, ascending=False)
    print('Najwieksza roznica miedzy rokiem 1910 a 2015 wystapila dla litery : ', df_res.head(1).index.values[0])

    letters = df_res.head(3).index.values
    df_res2 = df_backup.loc[letters]
    df_res3 = pd.pivot_table(df_res2, values='number', columns='last_letter',
                            index='year', aggfunc=np.sum)

    df_res3.plot(ax=axes[1])


def task_10():
    print('ZADANIE 10:')
    df_temp = df.groupby('name').nunique()
    df_unisex_names = df_temp.loc[df_temp['sex'] == 2]
    unisex_names = (list(df_unisex_names.index))    #lista imion nadawanych kobietom i mezczyznom

    df_10 = pd.merge(df, df_unisex_names, how='inner', on=['name'])
    df_res = df_10.groupby(['sex_x', 'name']).sum()
    df_res.sort_values(['number_x'], axis=0, inplace=True, ascending=False)

    print('najpopularniejsze imie meksie: \n', list(df_res.loc['M'].head(1).index)[0])
    print('najpopularniejsze imie zenskie: \n', list(df_res.loc['F'].head(1).index)[0], '\n')



def task_11():
    print('ZADANIE 11:')
    df_temp = df.sort_values('year')

    df_pom1 = df_temp.loc[df_temp['year'] <= 1920, :].groupby('name').nunique()
    df_pom1_1 = df_pom1.loc[df_pom1['sex'] == 2]
    df_1920 = pd.merge(df_temp, df_pom1_1,  how='inner', on=['name'])
    df_1920 = df_1920.groupby(['name', 'sex_x']).sum()
    res1920 = df_1920.groupby('name').sum()
    res1920['1880-1920 factor'] = df_1920['number_x'][:, 'F'].values / df_1920['number_x'][:, 'M'].values
    # print(res1920)

    df_pom2 = df_temp.loc[df_temp['year'] >= 2000, :].groupby('name').nunique()
    df_pom2_1 = df_pom2.loc[df_pom2['sex'] == 2]
    df_2000 = pd.merge(df_temp, df_pom2_1, how='inner', on=['name'])
    df_2000 = df_2000.groupby(['name', 'sex_x']).sum()
    res2000 = df_2000.groupby('name').sum()
    res2000['2000-2020 factor'] = df_2000['number_x'][:, 'F'].values / df_2000['number_x'][:, 'M'].values
    # print(res2000)

    res = pd.merge(res1920, res2000, how='inner', on=['name'])
    res['difference'] = res['2000-2020 factor'] - res['1880-1920 factor']
    print(res[['1880-1920 factor', '2000-2020 factor', 'difference']].sort_values('difference'), '\n')




def task_12():
    print('ZADANIE 12:')
    global df2
    conn = sqlite3.connect("USA_ltper_1x1.sqlite")
    df0 = pd.read_sql_query('SELECT Sex, Year, Age, mx, qx, ax, lx, dx, LLx, Tx, ex FROM USA_fltper_1x1 ORDER BY Year ASC', conn)
    df1 = pd.read_sql_query('SELECT Sex, Year, Age, mx, qx, ax, lx, dx, LLx, Tx, ex FROM USA_mltper_1x1 ORDER BY Year ASC', conn)
    conn.close()
    df2 = pd.concat([df0, df1])
    print(df2, '\n')


def task_13():
    print('ZADANIE 13: wykres')
    df_temp = df2.groupby('Year').sum()

    df_born = df.loc[df['year'] >= 1959]
    df_born = df_born.loc[df_born['year'] <= 2017].groupby('year').sum()
    df_temp['natural_increase'] = df_born['number'].values - df_temp['dx'].values # przyrost naturalny
    ax = df_temp.plot(kind='line', y='natural_increase', title='ZADANIE 13')



def task_14():
    print('ZADANIE 14: wykres')
    df_temp = df2.groupby(['Age', 'Year']).sum()
    df_temp2 = df2.groupby('Year').sum()
    df_born = df.loc[df['year'] >= 1959]
    df_born = df_born.loc[df_born['year'] <= 2017].groupby('year').sum()
    df_temp2['survivors0_factor'] = (df_born['number'].values - df_temp.loc[0, :]['dx'].values) / df_born['number'].values
    ax = df_temp2.plot(kind='line', y='survivors0_factor', title='ZADANIE 14')



if __name__ == '__main__':
    task_1()
    # task_2()
    # task_3()
    # task_4()
    # task_5()
    # top1000 = task_6()
    # task_7()
    # task_8(top1000) # korzysta z obliczen z task_6()
    # task_9()
    # task_10()
    # # task_11() #################### 3
    # task_12()
    # task_13()
    # task_14()
    # task_15() ################# 9
    plt.show()

    #8###################### ZAD 7
    ######################### uładnij wszystkie wykresy!
    #7###################### cos z funkcji do innej funkcji??
    #6###################### 13-15 zakres lat w jednej linijce
    #5###################### pusc wszystkie na raz, ogar zachowania
    #4###################### skontroluj czy wszystko z polecen
    # WYCZYSC I OBKOMENTUJ
    #instalacje pod labki