# Welcome to jRPI, Jake's Proprietary RPI gneration software.

# Import relevant packages
import pandas as pd
import sys
import numpy as np
import datetime as dt
import openpyxl
import matplotlib.pyplot as plt
import math

# Week of Rankings
week = 5

# Specify weights for input parameters. Values must sum to 1
w_adj_rpi = 0.5
w_rpi = 0
w_wl = 0
w_non_con = 0.05
w_con = 0.05
w_road = 0
w_last10 = 0.025
w_rpi25 = 0.1
w_rpi50 = 0.1
w_rpi100 = 0.075
w_rpi101 = 0.075
w_top100 = 0.025
w_bot150 = 0

weights = pd.Series([w_adj_rpi, w_rpi, w_wl, w_non_con, w_con, w_road, w_last10, w_rpi25, w_rpi50, w_rpi100, w_rpi101, w_top100, w_bot150],index=['Adj. RPI Value','RPI Value','WL%','Non-Conf%','Conf%','Road WL%','Last 10%','RPI25%','RPI50%','RPI100%','RPI101+%','Top100%','Below150%'])

if weights.sum() != 1:
    out_str = "ERROR CODE 1: Weights equal %f. Enter values that equal 1." %weights.sum()
    print(out_str)
    sys.exit()
else:

    d_season_jrpi = {}
    d_season_regs = {}
    last_in = {}
    for j in range(1,week+1):

        sheet = "Week_" + str(j)
        # Import data from NCAA Nitty Gritties website
        weekly_data = pd.read_excel('/Users/jakegrant/PycharmProjects/ACCTitles/NCAA_Softball_Selection_Data.xlsx',sheet_name=sheet,engine='openpyxl')

        # Calculate Win Percentage
        try:
            weekly_data['WL%'] = (weekly_data['WL'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['WL'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['WL'].str.split('-', expand=True)[0].astype(int) + weekly_data['WL'].str.split('-', expand=True)[1].astype(int) + weekly_data['WL'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['WL%'] = weekly_data['WL'].str.split('-', expand=True)[0].astype(int)/(weekly_data['WL'].str.split('-', expand=True)[0].astype(int) + weekly_data['WL'].str.split('-', expand=True)[1].astype(int))

        # Calculate Non-Conference Win Percentage
        try:
            weekly_data['Non-Conf%'] = (weekly_data['Non-Conf Record'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['Non-Conf Record'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['Non-Conf Record'].str.split('-', expand=True)[0].astype(int) + weekly_data['Non-Conf Record'].str.split('-', expand=True)[1].astype(int) + weekly_data['Non-Conf Record'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['Non-Conf%'] = weekly_data['Non-Conf Record'].str.split('-', expand=True)[0].astype(int) / (weekly_data['Non-Conf Record'].str.split('-', expand=True)[0].astype(int) + weekly_data['Non-Conf Record'].str.split('-', expand=True)[1].astype(int))

        # Calculate Conference Win Percentage
        try:
            weekly_data['Conf%'] = (weekly_data['Conf. Record'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['Conf. Record'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['Conf. Record'].str.split('-', expand=True)[0].astype(int) + weekly_data['Conf. Record'].str.split('-', expand=True)[1].astype(int) + weekly_data['Conf. Record'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['Conf%'] = weekly_data['Conf. Record'].str.split('-', expand=True)[0].astype(int) / (weekly_data['Conf. Record'].str.split('-', expand=True)[0].astype(int) + weekly_data['Conf. Record'].str.split('-', expand=True)[1].astype(int))

        # Calculate Road Win Percentage
        try:
            weekly_data['Road WL%'] = (weekly_data['Road WL'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['Road WL'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['Road WL'].str.split('-', expand=True)[0].astype(int) + weekly_data['Road WL'].str.split('-', expand=True)[1].astype(int) + weekly_data['Road WL'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['Road WL%'] = weekly_data['Road WL'].str.split('-', expand=True)[0].astype(int) / (weekly_data['Road WL'].str.split('-', expand=True)[0].astype(int) + weekly_data['Road WL'].str.split('-', expand=True)[1].astype(int))

        # Calculate Last 10 Games Win Percentage
        try:
            weekly_data['Last 10%'] = (weekly_data['Last 10 Games'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['Last 10 Games'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['Last 10 Games'].str.split('-', expand=True)[0].astype(int) + weekly_data['Last 10 Games'].str.split('-', expand=True)[1].astype(int) + weekly_data['Last 10 Games'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['Last 10%'] = weekly_data['Last 10 Games'].str.split('-', expand=True)[0].astype(int) / (weekly_data['Last 10 Games'].str.split('-', expand=True)[0].astype(int) + weekly_data['Last 10 Games'].str.split('-', expand=True)[1].astype(int))

        # Calculate Win Percentage vs. Top 25 RPI Teams
        try:
            weekly_data['RPI25%'] = (weekly_data['RPI 1-25'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['RPI 1-25'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['RPI 1-25'].str.split('-', expand=True)[0].astype(int) + weekly_data['RPI 1-25'].str.split('-', expand=True)[1].astype(int) + weekly_data['RPI 1-25'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['RPI25%'] = weekly_data['RPI 1-25'].str.split('-', expand=True)[0].astype(int) / (weekly_data['RPI 1-25'].str.split('-', expand=True)[0].astype(int) + weekly_data['RPI 1-25'].str.split('-', expand=True)[1].astype(int))

        # Calculate Win Percentage vs. 26-50 Ranked RPI Teams
        try:
            weekly_data['RPI50%'] = (weekly_data['RPI 26-50'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['RPI 26-50'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['RPI 26-50'].str.split('-', expand=True)[0].astype(int) + weekly_data['RPI 26-50'].str.split('-', expand=True)[1].astype(int) + weekly_data['RPI 26-50'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['RPI50%'] = weekly_data['RPI 26-50'].str.split('-', expand=True)[0].astype(int) / (weekly_data['RPI 26-50'].str.split('-', expand=True)[0].astype(int) + weekly_data['RPI 26-50'].str.split('-', expand=True)[1].astype(int))

        # Calculate Win Percentage vs. 51-100 Ranked RPI Teams
        try:
            weekly_data['RPI100%'] = (weekly_data['RPI 51-100'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['RPI 51-100'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['RPI 51-100'].str.split('-', expand=True)[0].astype(int) + weekly_data['RPI 51-100'].str.split('-', expand=True)[1].astype(int) + weekly_data['RPI 51-100'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['RPI100%'] = weekly_data['RPI 51-100'].str.split('-', expand=True)[0].astype(int) / (weekly_data['RPI 51-100'].str.split('-', expand=True)[0].astype(int) + weekly_data['RPI 51-100'].str.split('-', expand=True)[1].astype(int))

        # Calculate Win Percentage vs. >100 Ranked RPI Teams
        try:
            weekly_data['RPI101+%'] = (weekly_data['RPI 101+'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['RPI 101+'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['RPI 101+'].str.split('-', expand=True)[0].astype(int) + weekly_data['RPI 101+'].str.split('-', expand=True)[1].astype(int) + weekly_data['RPI 101+'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['RPI101+%'] = weekly_data['RPI 101+'].str.split('-', expand=True)[0].astype(int) / (weekly_data['RPI 101+'].str.split('-', expand=True)[0].astype(int) + weekly_data['RPI 101+'].str.split('-', expand=True)[1].astype(int))

        # Calculate Win Percentage vs. Top 100 RPI Teams
        try:
            weekly_data['Top100%'] = (weekly_data['vs TOP 100'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['vs TOP 100'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['vs TOP 100'].str.split('-', expand=True)[0].astype(int) + weekly_data['vs TOP 100'].str.split('-', expand=True)[1].astype(int) + weekly_data['vs TOP 100'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['Top100%'] = weekly_data['vs TOP 100'].str.split('-', expand=True)[0].astype(int) / (weekly_data['vs TOP 100'].str.split('-', expand=True)[0].astype(int) + weekly_data['vs TOP 100'].str.split('-', expand=True)[1].astype(int))

        # Calculate Win Percentage vs. Bottom 150 RPI Teams
        try:
            weekly_data['Below150%'] = (weekly_data['vs below 150'].str.split('-', expand=True)[0].astype(int) + .5*weekly_data['vs below 150'].str.split('-', expand=True)[2].fillna(0).astype(int))/(weekly_data['vs below 150'].str.split('-', expand=True)[0].astype(int) + weekly_data['vs below 150'].str.split('-', expand=True)[1].astype(int) + weekly_data['vs below 150'].str.split('-', expand=True)[2].fillna(0).astype(int))
        except KeyError:
            weekly_data['Below150%'] = weekly_data['vs below 150'].str.split('-', expand=True)[0].astype(int) / (weekly_data['vs below 150'].str.split('-', expand=True)[0].astype(int) + weekly_data['vs below 150'].str.split('-', expand=True)[1].astype(int))

        # Calculate jRPI and Rank
        weekly_vals = weekly_data.drop(['Team','Conference','SOS','Prev SOS','Adj. RPI','RPI','WL','Adj. Non-Conf RPI','Non-Conf Record','Conf RPI','Conf. Record','Road WL','Last 10 Games','RPI 1-25','RPI 26-50','RPI 51-100','RPI 101+','vs TOP 100','vs below 150','NC SOS'],axis=1).fillna(0)
        weekly_jrpi = pd.DataFrame(weekly_vals.dot(weights), columns={'jRPI'})
        weekly_jrpi['Team'] = weekly_data['Team']
        weekly_jrpi['Conference'] = weekly_data['Conference']
        column_names = ['Team', 'Conference', 'jRPI']
        weekly_jrpi = weekly_jrpi.reindex(columns=column_names)
        weekly_jrpi['Rank'] = weekly_jrpi['jRPI'].rank(ascending=False)
        weekly_jrpi = weekly_jrpi.sort_values(by=['Rank']).reset_index(drop=True)

        # Find Autobids
        autos = weekly_jrpi.sort_values('Rank').groupby('Conference', as_index=False).first()['Team']
        weekly_jrpi['Autos'] = weekly_jrpi['Team'].isin(autos)

        # Find At Larges
        weekly_jrpi['At Large'] = weekly_jrpi.loc[weekly_jrpi['Autos'] == False, 'Rank']
        at_larges = weekly_jrpi.nsmallest(32, 'At Large', keep='first')['Team']
        last_in["last_{0}".format(j)] = at_larges.index[-1]
        weekly_jrpi['At Large'] = weekly_jrpi['Team'].isin(at_larges)

        # Determine Teams in Field
        weekly_jrpi['Field'] = weekly_jrpi['Autos'] | weekly_jrpi['At Large']
        tourney_field = weekly_jrpi.loc[weekly_jrpi['Field'] == True].reset_index(drop=True)

        # Regionals:
        team_pool = tourney_field
        d_regs = {}
        for i in range(16):
            seed_1 = team_pool.iloc[[0]]
            d_regs["reg_{0}".format(i)] = seed_1
            team_pool = team_pool[~team_pool['Team'].isin(seed_1['Team'])]

        for i in range(15,-1,-1):
            opt_1 = d_regs["reg_{0}".format(i)]
            valid_1 = opt_1['Conference']

            seed_2_ops = team_pool[~team_pool['Conference'].isin(valid_1)]
            seed_2 = seed_2_ops.iloc[[0]]
            d_regs["reg_{0}".format(i)] = pd.concat([opt_1,seed_2])
            team_pool = team_pool[~team_pool['Team'].isin(seed_2['Team'])]

        for i in range(16):
            opt_1_2 = d_regs["reg_{0}".format(i)].reset_index(drop=True)
            valid_1 = [opt_1_2['Conference'][0]]
            valid_2 = [opt_1_2['Conference'][1]]

            seed_3_ops = team_pool[~team_pool['Conference'].isin(valid_1)]
            seed_3_ops = seed_3_ops[~seed_3_ops['Conference'].isin(valid_2)]
            seed_3 = seed_3_ops.iloc[[0]]
            d_regs["reg_{0}".format(i)] = pd.concat([opt_1_2, seed_3])
            team_pool = team_pool[~team_pool['Team'].isin(seed_3['Team'])]

        for i in range(15, -1, -1):
            opt_1_2_3 = d_regs["reg_{0}".format(i)].reset_index(drop=True)
            valid_1 = [opt_1_2_3['Conference'][0]]
            valid_2 = [opt_1_2_3['Conference'][1]]
            valid_3 = [opt_1_2_3['Conference'][2]]

            seed_4_ops = team_pool[~team_pool['Conference'].isin(valid_1)]
            seed_4_ops = seed_4_ops[~seed_4_ops['Conference'].isin(valid_2)]
            seed_4_ops = seed_4_ops[~seed_4_ops['Conference'].isin(valid_3)]
            seed_4 = seed_4_ops.iloc[[0]]
            d_regs["reg_{0}".format(i)] = pd.concat([opt_1_2_3, seed_4]).reset_index(drop=True)
            team_pool = team_pool[~team_pool['Team'].isin(seed_4['Team'])]

        for key in d_regs:
            if len(d_regs[key]) < 4:
                out_str = "ERROR CODE 2: Invalid regional output. Adjust parameters for proper 4 team assignments (SEC error)."
                error_week = "Issue in Week %f" %j
                print(d_regs)
                print(out_str)
                print(error_week)
                sys.exit()

        d_season_jrpi["reg_{0}".format(j)] = weekly_jrpi.set_index('Team')
        d_season_regs["reg_{0}".format(j)] = d_regs

    # Assemble Master jRPI and Ranks Sheets
    season_jrpis = pd.DataFrame()
    season_ranks = pd.DataFrame()

    k = 0
    for key in d_season_jrpi:
        k += 1
        jrpi_rank = d_season_jrpi[key].drop(['Conference','Autos','At Large','Field'],axis=1)
        season_jrpis['Week {}'.format(k)] = jrpi_rank['jRPI']
        season_ranks['Week {}'.format(k)] = jrpi_rank['Rank']

    field_jrpis = season_jrpis[season_jrpis.index.isin(tourney_field['Team'])]
    field_ranks = season_ranks[season_ranks.index.isin(tourney_field['Team'])]

    # Plot of jRPI, Rank with Tech Highlighted
    # jRPI
    my_dpi = 96
    fig_val = 600
    fig1, ax = plt.subplots()
    plt.style.use('seaborn-darkgrid')
    plt.figure(figsize=(fig_val / my_dpi, fig_val / my_dpi), dpi=my_dpi)
    plt.plot(season_jrpis.T,marker='', color='grey', linewidth=1, alpha=0.4)
    plt.plot(season_jrpis.T['Georgia Tech'], marker='', color='#b3a369', linewidth=4, alpha=0.7)
    plt.ylim(bottom=0)
    plt.ylabel('jRPI Rating')
    plt.title('Weekly Change in jRPI Rating')
    plt.text(1, -0.1, 'Jake Grant, 2022', horizontalalignment='right',
             verticalalignment='center', transform=ax.transAxes)
    jRPI_fig = 'jRPI_plot.png'
    plt.savefig(jRPI_fig,dpi=my_dpi)
    #plt.show()

    # Rank
    fig2, ax = plt.subplots()
    plt.style.use('seaborn-darkgrid')
    plt.figure(figsize=(fig_val / my_dpi, fig_val / my_dpi), dpi=my_dpi)
    plt.plot(season_ranks.T, marker='', color='grey', linewidth=1, alpha=0.4)
    plt.plot(season_ranks.T['Georgia Tech'], marker='', color='#b3a369', linewidth=4, alpha=0.7)
    plt.plot(pd.DataFrame(list(last_in.items())).drop([0], axis=1), marker='', color='black', linewidth=2,
             alpha=0.7)
    plt.ylim(bottom=0)
    plt.gca().invert_yaxis()
    plt.ylabel('jRPI Ranking')
    plt.title('Weekly Change in jRPI Ranking')
    plt.text(1, -0.1, 'Jake Grant, 2022', horizontalalignment='right',
             verticalalignment='center', transform=ax.transAxes)
    rank_fig = 'rank_plot.png'
    plt.savefig(rank_fig,dpi=my_dpi)
    #plt.show()

    # Plot of jRPI, Rank for CURRENT Tournament Teams
    # jRPI
    my_dpi = 96
    fig_val = 600
    fig3, ax = plt.subplots()
    plt.style.use('seaborn-darkgrid')
    plt.figure(figsize=(fig_val / my_dpi, fig_val / my_dpi), dpi=my_dpi)
    plt.plot(field_jrpis.T, marker='', color='grey', linewidth=1, alpha=0.4)
    try:
        plt.plot(field_jrpis.T['Georgia Tech'], marker='', color='#b3a369', linewidth=4, alpha=0.7)
    except KeyError:
        print('ERROR CODE 3: Tech not in tournament field. Code will proceed.')
    plt.ylim(bottom=0)
    plt.ylabel('jRPI Rating')
    plt.title('Weekly Change in jRPI Rating for Tournament Teams')
    plt.text(1, -0.1, 'Jake Grant, 2022', horizontalalignment='right',
             verticalalignment='center', transform=ax.transAxes)
    jRPI_fig = 'jRPI_field_plot.png'
    plt.savefig(jRPI_fig, dpi=my_dpi)
    #plt.show()

    # Rank
    my_dpi = 96
    fig_val = 600
    fig4, ax = plt.subplots()
    plt.style.use('seaborn-darkgrid')
    plt.figure(figsize=(fig_val / my_dpi, fig_val / my_dpi), dpi=my_dpi)
    plt.plot(field_ranks.T, marker='', color='grey', linewidth=1, alpha=0.4)
    try:
        plt.plot(field_ranks.T['Georgia Tech'], marker='', color='#b3a369', linewidth=4, alpha=0.7)
        plt.plot(pd.DataFrame(list(last_in.items())).drop([0], axis=1), marker='', color='black', linewidth=2,
                 alpha=0.7)
    except KeyError:
        plt.plot(pd.DataFrame(list(last_in.items())).drop([0], axis=1), marker='', color='black', linewidth=2,
                 alpha=0.7)
    plt.ylim(bottom=0)
    plt.gca().invert_yaxis()
    plt.ylabel('jRPI Ranking')
    plt.title('Weekly Change in jRPI Ranking for Tournament Teams')
    plt.text(1, -0.1, 'Jake Grant, 2022', horizontalalignment='right',
             verticalalignment='center', transform=ax.transAxes)
    rank_fig = 'rank_field_plot.png'
    plt.savefig(rank_fig, dpi=my_dpi)
    #plt.show()

    # NEXT: ACC TEAM PLOT (WITH COLOR?)


    # Writer Outputs to Excel
    tourney_projection = pd.concat(d_regs)
    out_xls_name = 'Week_' + str(k) + '_Tourney_Prediction.xlsx'
    with pd.ExcelWriter(out_xls_name) as writer:
        tourney_projection.to_excel(writer, sheet_name='Projected Field')
        blank = pd.DataFrame()
        blank.to_excel(writer, sheet_name='jRPI Plot')
        blank.to_excel(writer, sheet_name='Rank Plot')

    # Print jRPI Plot to File
    wb = openpyxl.load_workbook(out_xls_name)
    ws = wb['jRPI Plot']
    img = openpyxl.drawing.image.Image(jRPI_fig)
    img.anchor = 'A1'  # Or whatever cell location you want to use.
    ws.add_image(img)
    wb.save(out_xls_name)

    # Print Rank Plot to File
    wb = openpyxl.load_workbook(out_xls_name)
    ws = wb['Rank Plot']
    img = openpyxl.drawing.image.Image(rank_fig)
    img.anchor = 'A1'  # Or whatever cell location you want to use.
    ws.add_image(img)
    wb.save(out_xls_name)

#### SCRATCH WORK ####


    # Unused Code to Add Plot Labels
    #num = 0
    #for i in df.values[9][1:]:
    #    num += 1
    #    name = list(df)[num]
    #    if name != 'y5':
    #        plt.text(10.2, i, name, horizontalalignment='left', size='small', color='grey')
    # Call Out Tech
    #plt.text(10.2, season_jrpis.T['Georgia Tech'].tail(1), 'Georgia Tech', horizontalalignment='left', size='small', color='#b3a369')

# Plot jRPI vs RPI, WL%, etc.
# plot of teams in vs. out (like show which ones have been in the whole team vs. not? idk

