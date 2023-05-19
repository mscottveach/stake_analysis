import build_database
import build_viz
import sqlite3
from sqlite3 import Error
import os, json
from datetime import datetime
import pandas as pd
import build_report
from fpdf import FPDF
import contextlib

# Stake Betting History
# mscottveach@gmail.com
#
# Period Covered: 02/12/21 - 01/09/22
# Total Number of Bets: 23,003
# Total Amount Wagered: $53,4233.00
# Total Pofit/Loss: -$3,400.00
# Biggest Win: Deadwood for $2000.00 on 4/12/21
# Most Played Game: Plinko
#
# [LIFETIME PROFIT/LOSS CHART]
#
# PER GAME STATISTICS:
# Game: Deadwood
# Provide: NoLimit
# Number of bets: 242
# Total Amount Wagered: $504.00
# 5 Biggest Wins:
#   $2000 on 4/12/21
#   $123 on 3/01/21
#   $9 on 11/23/21
#
# [GAME SPECIFIC PROFIT/LOSS CHART]
#
# Repeat for Every Game in Database


# ID, DATE, UNIX, GAME, CURRENCY, BET, BET VALUE IN USD, BET PAYOUT, PROVIDER, BONUS, CATEGORY, BET PROFIT, BET #, BET PROFIT RT, BET RT

client_name = 'Syztmz'
period_covered = ''
total_number_of_bets = 0
total_wagered = 0
total_profit = 0
pdf = 0

class PDF:


    def titles(self):
        self.set_xy(210.0, 20.0)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0,0,0)
        self.cell(w=210.0, h=5.0, align='L', txt="STAKE BETTING HISTORY", ln=1, border=0)
        self.set_font('Helvetica', '', 10)
        self.cell(w=210.0, h=5.0, align='L', txt=client_name, ln=1, border=0)

    def print_line(self,in_line):
        self.cell(w=210.0, h=5.0, align='L', txt=in_line, ln=1, border=0)

    def print_title(self, in_line):
        self.set_font('Helvetica', 'B', 12)
        self.cell(w=210.0, h=5.0, align='L', txt=in_line, ln=1, border=0)
        self.set_font('Helvetica', '', 10)


    def insert_image(self, in_img_name):
        self.image(in_img_name,x=0,y=0,w=8)

class report():
    def __init__(self, file_name):
        self.t = open(file_name, 'w')

    def close(self):
        if self.t:
            self.t.close()
            self.t = None


def generate_data_frame(conn):
    cursor = conn.cursor()
    sql_qry = "select * from the_bets order by bet_date_unix"
    cursor.execute(sql_qry)
    all_bets = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(all_bets)
    df.rename(columns={0: 'ID', 1: 'DATE', 2: 'UNIX', 3: 'GAME', 4: 'CURRENCY', 5: 'BET', 6: 'BET VALUE IN USD',
                       7: 'BET PAYOUT', 8: 'PROVIDER', 9: 'BONUS', 10: 'CATEGORY'}, inplace=True)

    #remove no money bets
    df.drop(df.index[df['BET'] == 0], inplace=True)

    bet_count = []
    cnt = 0
    for elem in df.index:
        cnt += 1
        bet_count.append(cnt)
    df['BET #'] = bet_count
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
    return df

def generate_running_totals(in_df):

    df = in_df.copy()
    profit_per_bet = []
    bet_count = []
    total_profit_rt = []
    bet_rt = []
    cnt = 0
    total_profit = 0
    max_profit = 0
    min_profit = 0
    bet_val_rt = 0

    for elem in df.index:
        bet_amt = df['BET'][elem]
        bet_val = df['BET VALUE IN USD'][elem]
        curr2usd = float(bet_val) / float(bet_amt)
        bet_pay = df['BET PAYOUT'][elem] * curr2usd
        bet_profit = bet_pay - bet_val
        total_profit += bet_profit
        bet_val_rt += bet_val

        bet_rt.append(bet_val_rt)
        profit_per_bet.append(bet_profit)
        bet_count.append(cnt)
        total_profit_rt.append(total_profit)

    df['BET PROFIT'] = profit_per_bet
    df['BET #'] = bet_count
    df['BET PROFIT RT'] = total_profit_rt
    df['BET RT'] = bet_rt
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
    #print(df.head())
    return df

def print_line(f, string):
    f.write(string+'  \n')

def print_title(f, string):
    f.write('**'+string+'**  \n')

def insert_image(f, string):
    f.write('![graph](./'+string+' "Graph")\n')


def make_header(in_f):
    f = in_f
    print_line(f,'<h2>Stake Betting History</h2>\n\n')


def calc_everything(df, header, in_f, make_graph):
    global period_covered
    global total_number_of_bets
    global total_wagered
    global total_profit

    from_date = df.iloc[0]['DATE'].date()
    to_date = df.iloc[-1]['DATE'].date()
    period_covered = str(from_date) + ' - ' + str(to_date)
    total_number_of_bets = len(df.index)
    total_wagered = df.iloc[-1]['BET RT']
    total_profit = df.iloc[-1]['BET PROFIT RT']
    f = in_f
    print_title(f,header)
    print_line(f,'Period covered: ' + period_covered)
    tot_num_bets_str = f'Total number of bets: {int(total_number_of_bets):,}'
    print_line(f,tot_num_bets_str)
    tot_wag_str = f'Total Amount Wagered: ${total_wagered:,.2f}'
    print_line(f,tot_wag_str)
    tot_pro_str = f'Total Profit ${total_profit:,.2f}'
    print_line(f,tot_pro_str)
    print_line(f,'')

    if make_graph:
        a_plot_name = build_viz.viz_go(df,header)
        insert_image(f, a_plot_name)




def calc_casino_only(df):
    casino_df = df[df['CATEGORY'] != 'sportsbook']
    return(casino_df)

def calc_sports_only(df):
    sports_df = df[df['CATEGORY'] == 'sportsbook']
    return(sports_df)

def generate_list_of_games():
    pass

def generate_csv(df):
    df.to_csv(email+'.csv',index=False)

def init_pdf():
    global pdf
    pdf = PDF('P','in')
    #pdf.add_page()
    pdf.titles()
#    pdf.output('output.pdf')
    return(pdf)

def write_pdf(in_pdf):
    in_pdf.output('report.pdf')

def get_game_list(df):
    list_of_games = set()
    for elem in df.index:
        list_of_games.add(df['GAME'][elem])
    return list_of_games