
originals = ['plinko', 'mines', 'hilo', 'dice', 'crash', 'limbo']

def return_provider_name(in_string):
    if in_string == 'plinko':
        provider = 'original'
    elif ':' in in_string:
        provider, game_name = in_string.split(':')
    else:
        provider = ''

    return provider

