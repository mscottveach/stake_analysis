import build_database
import build_viz
import sqlite3
from sqlite3 import Error
import os, json
from datetime import datetime
import pandas as pd
import build_report




if __name__ == '__main__':

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)
    cust_name = 'veach'
    cust_db = ".\sqlite_db\stake_bets-"+cust_name+".db"
    cust_db = ".\sqlite_db\stake_bets.db"

    #conn = build_database.go(cust_db)

    conn = sqlite3.connect(cust_db)
    df_all = build_report.generate_data_frame(conn)
    df_all = build_report.generate_running_totals(df_all)


    df_casino = build_report.calc_casino_only(df_all)
    df_casino = build_report.generate_running_totals(df_casino)

    df_sports = build_report.calc_sports_only(df_all)
    df_sports = build_report.generate_running_totals(df_sports)

    #pdf = build_report.init_pdf()
    f = open('report.md', 'w')
    build_report.make_header(f)

    build_report.calc_everything(df_all, 'All Bets', f, True)
    build_report.calc_everything(df_casino, 'Casino', f, True)
    build_report.calc_everything(df_sports, 'Sportsbook', f, True)

    list_of_games = build_report.get_game_list(df_casino)
    for game in list_of_games:
        game_df = df_all[df_all['GAME'] == game]
        print(game, len(game_df))
        game_df = build_report.generate_running_totals(game_df)
        build_report.calc_everything(game_df, game, f, False)


    #build_report.write_pdf(f)
    f.close()


    #build_report.generate_csv(df)




 #   build_viz.viz_go(conn, df)

