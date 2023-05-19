import math
import random
import statistics

KEYS = [.2, 2, 4, 9, 26, 130, 1000]
HIT_COUNTS = {.2:0, 2:0, 4:0, 9:0, 26:0, 130:0, 1000:0}
PLINKO_PMF = {}
NUM_OF_TRIALS_1 = 811596
NUM_OF_TRIALS_2 = 102153
NUM_OF_TRIALS_3 = 79700
NUM_OF_TRIALS_4 = 22453
NUM_OF_TRIALS_5 = 818848
NUM_OF_TRIALS_6 = 100000
NUM_OF_TRIALS = NUM_OF_TRIALS_6
# THE_PMF = DICE_PMF
THE_PMF = PLINKO_PMF
EXP_COUNT = {}
SYZ_COUNT_1 = {.2: 640069, 2: 108158, 4: 45266, 9: 13717, 26: 3000, 130: 430, 1000: 25}
SYZ_COUNT_2 = {.2: 80905, 2: 10565 + 2916, 4: 4401 + 1254, 9: 1341 + 331, 26: 304 + 93, 130: 36 + 7, 1000:0}
SYZ_COUNT_3 = {.2: 63053, 2: 10565, 4: 4401, 9:1341, 26: 304,130: 36,1000: 0}
SYZ_COUNT_4 = {.2: 17852, 2: 2916, 4: 1254, 9: 331, 26: 93, 130: 7, 1000:0}
SYZ_COUNT_5 = {.2: 650519, 2:106550, 4: 45077, 9: 13349, 26: 2898, 130: 428, 1000: 27}
SYZ_COUNT = SYZ_COUNT_1
EXP_RETURN = 0

def calc_sd():
    global SD
    global EXP_RETURN
    # u is the expected value, obtained via the formula SUM(value*probability_of_value)
    u = 0
    a_sum = 0
    for key in THE_PMF:
        u += key*THE_PMF[key]
        a_sum += THE_PMF[key]
    v = 0
    for key in THE_PMF:
        v += THE_PMF[key]*((key - u)**2)

    print("Expected value is: ", u)
    print("Variance is: ", v)
    print("Number of trials is: ", NUM_OF_TRIALS)
    #print("Expected value for those trials is: ", NUM_OF_TRIALS * u)
    print("Variance for those trials is: ", v * NUM_OF_TRIALS)
    print("Standard deviation for those trials is:", math.sqrt(v*NUM_OF_TRIALS))
    sd = math.sqrt(v*NUM_OF_TRIALS)
    SD = sd
    TRIAL_RETURN = 0
    SYZ_RETURN = 0
    for key, val in PLINKO_PMF.items():
        EXP_COUNT[key] = val * NUM_OF_TRIALS
        TRIAL_RETURN += key*(val * NUM_OF_TRIALS)
        SYZ_RETURN += SYZ_COUNT[key] * key
    print("Expected number of individual hits for those trials is:")
    print(EXP_COUNT)
    print("Expected return is: ", TRIAL_RETURN)
    EXP_RETURN = TRIAL_RETURN
    print("Syz's actual return is: ", SYZ_RETURN)
    print("Which is a loss off expected return of: ",SYZ_RETURN - TRIAL_RETURN)
    print("")
    print("68% of the time someone drops ", NUM_OF_TRIALS," trials they should be within ", sd, " of ", TRIAL_RETURN)
    print("95% of the time someone drops ", NUM_OF_TRIALS," trials they should be within ", 2*sd, " of ", TRIAL_RETURN)
    print("99.7% of the time someone drops ", NUM_OF_TRIALS, " they should be within ", 3*sd, " of ", TRIAL_RETURN)





def get_head_count():
    head_count = 0
    tail_count = 0
    for idx in range(0,16):
        a_flip = random.random()
        if a_flip <= .5:
            head_count += 1
        else:
            tail_count += 1
    return(max(head_count,tail_count))

def plinko_counter_simulator():
    reward = 0
    current_hits = HIT_COUNTS.copy()
    for drop in range(0, NUM_OF_TRIALS):
        num_of_heads = get_head_count()
        index = num_of_heads - 10
        if index < 0:
            index = 0
        current_hits[KEYS[index]] += 1

    return (current_hits)

def heads_to_multiplier(in_head_count):
    index = in_head_count - 10
    if index < 0:
        index = 0

    return KEYS[index]

def sim_rev_martingale_on_plinko(in_bets_to_double, num_of_trials):
    reward = 0
    current_hits = HIT_COUNTS.copy()
    do_i_inc_bet = False
    bet = 10
    inc_bet_by = 1
    bankroll = 100000
    max_bankroll = 0
    max_jump = 0
    a_str = []
    for drop in range(0, NUM_OF_TRIALS):
        if do_i_inc_bet > 0:
            do_i_inc_bet -= 1
            bet = inc_bet_by * bet
        elif do_i_inc_bet == 0:
            bet = 10
            inc_bet_by = 1

        bankroll -= bet
        num_of_heads = get_head_count()
        index = num_of_heads - 10
        if index < 0:
            index = 0
        current_hits[KEYS[index]] += 1
        bankroll += KEYS[index]*bet
        if KEYS[index]*bet > max_jump:
            max_jump = KEYS[index]*bet


        if KEYS[index] in in_bets_to_double:
            a_str.append(str("Drop #" + str(drop) + "  Bankroll: " + str(bankroll) + "Just hit: " + str(KEYS[index]) + "Bet size: " + str(bet)))
            do_i_inc_bet = True
            inc_bet_by = KEYS[index]
        else:
            a_str =[]
            do_i_inc_bet = False

        if len(a_str) == 3:
            do_i_inc_bet = False
            inc_bet_by = 1
            for elem in a_str:
                #print(elem)
                pass
        else:
            pass
            #print("Drop #",drop," Bankroll: ",bankroll)

        if bankroll > max_bankroll:
            max_bankroll = bankroll

    return (bankroll, max_bankroll, max_jump)

def compute_pmf():
    # the chances of flipping heads 16 times in a row or tails 16 times in a row:
    PLINKO_PMF[1000] = (.5**16)*2
    # x1000 is also the chance of any particular arrangement of flips.

    # 16 choose 1 * chances of x1000
    PLINKO_PMF[130] = 16*PLINKO_PMF[1000]
    # 16 choose 2 * chances of x1000
    PLINKO_PMF[26] = 120*PLINKO_PMF[1000]
    # 16 choose 3 * chances of x1000
    PLINKO_PMF[9] = 560*PLINKO_PMF[1000]
    # 16 choose 4 * chances of x1000
    PLINKO_PMF[4] = 1820*PLINKO_PMF[1000]
    # 16 choose 5 * chances of x1000
    PLINKO_PMF[2] = 4368*PLINKO_PMF[1000]
    # 16 choose 6 + 16 choose 7 + ((16 choose 8)/2) * x1000
    PLINKO_PMF[.2] = 25883*PLINKO_PMF[1000]

def test_pmf():
    total = 0
    for key, val in PLINKO_PMF.items():
        total += val
    print("Summation of probabilities is: ", total)

if __name__ == '__main__':
    random.seed()

    count = 0
    last_thou = 0
    hold_dist = []
    for sim_num in range(0,10000000):
        heads = get_head_count()
        count += 1
        multi = heads_to_multiplier(heads)
        if multi == 26:
            dist = count - last_thou
            #print(f'Drops since last 1000x: {dist}')
            hold_dist.append(dist)
            last_thou = count

    print("")
    print(f'Avg distance: {statistics.mean(hold_dist)}')
    print(f'Std Deviation: {statistics.stdev(hold_dist)}')
    print(f'Max distance: {max(hold_dist)}')
    print(f'Min Distance: {min(hold_dist)}')