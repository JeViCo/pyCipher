from math import sqrt, ceil
from string import ascii_uppercase
from NumpyHill import hill_cip
from rsa import keyGen, encrypt, decrypt

# Общее
def toHex ( n ):
    return '{0:02x}'.format ( n )

def fromHex ( n ):
    return int ( n, 16 )

# Магический квадрат
def nearest_square ( n ):
    #sq =  int ( sqrt ( ceil ( sqrt ( n ) ) ** 2 ) )
    sq = ceil ( sqrt ( n ) )
    if ( sq%2 == 0 ): # Только нечётные
        sq += 1
    return sq

def create_magic_square ( num ): # Создаём магический квадрат размерностью num X num
    N = nearest_square ( num )
    arr = [ [ '' for x in range(N) ] for y in range(N) ] 

    n = 1
    i, j = 0, N//2
    
    while n <= N**2:
        arr[ i ][ j ] = n
        n += 1
        newi, newj = (i-1) % N, (j+1)% N
        if arr[ newi ][ newj ]:
            i += 1
        else:
            i, j = newi, newj
    return [ arr, N ]

def magic_square ( s, rev ): # Корректная реализация. Повторная прогонка для длинных слов не даёт нужного результата
    l = len ( s )
    output = ''
    spec_char = '_'
    square = create_magic_square ( l )

    Matrix, size = square[ 0 ], square[ 1 ]
    toCip = s + ( spec_char * ( size**2 - l ) )

    if rev:
        output = [ '' for x in range ( size**2 ) ]
        toCip = [ s[ i:i+size ] for i in range(0, len(s), size)]

    for i in range ( size ):
        for j in range ( size ):
            if rev:
                output[ Matrix[ i ][ j ] - 1 ] = toCip[ i ][ j ]
            else:
                output += toCip[ Matrix[ i ][ j ] - 1 ]

    return ''.join ( output ).replace ( spec_char, '' ) if rev else output

# Гаммирование

def gamma ( s, rev ):
    key = 'мойключ'
    key += key * ceil ( len ( s ) / len ( key ) ) # Расширяем
    toCip = [ ]
    if rev:
        sp = s.split()
        for i in range ( len ( sp ) ):
            toCip += [ chr ( fromHex ( sp[ i ]  ) ^ ord ( key[ i ] ) ) ]
            #toCip += [ chr ( ord ( sp[ i ] ) ^ ord ( key[ i ] ) ) ]
    else:
        for i in range ( len ( s ) ):
            toCip += [ toHex ( ( ord ( s[ i ] ) ^ ord ( key[ i ] ) ) ) ]
            #toCip += [ chr ( ( ord ( s[ i ] ) ^ ord ( key[ i ] ) ) ) ]

    return ('' if rev else ' ').join ( toCip )
    #return ''.join ( toCip )

# Комбинированный ( ADFGVX )
ADFGVX_en = { }
ADFGVX_ru = { }
alphabet_en = list ( ascii_uppercase )
alphabet_ru = list ( 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ' )

def ADFGVXgen ( ):
    key = [ 'A', 'D', 'F', 'G', 'V', 'H' ]

    for i in range ( len ( key ) ):
        for j in range ( len ( key ) ):
            # RU
            ADFGVX_ru[ key[ i ] + key[ j ] ] = alphabet_ru [ 0 ] if len ( alphabet_ru ) > 0 else '-'
            if len ( alphabet_ru ) > 0:
                alphabet_ru.pop ( 0 )
            #EN
            ADFGVX_en[ key[ i ] + key[ j ] ] = alphabet_en [ 0 ] if len ( alphabet_en ) > 0 else '-'
            if len ( alphabet_en ) > 0:
                alphabet_en.pop ( 0 )

ADFGVXgen ( )

def dictSearch ( v, dic ):
    for key, val in dic.items():
        if val == v:
            return key

def combine_cip ( s, rev ):
    source = s.upper ( ).split ( ) if rev else s.upper ( )
    toCip = [ ]

    for i in range ( len ( source ) ):
        letter = ''
        if rev:
            letter = ADFGVX_ru [ source[ i ] ].lower ( )
        else:
            letter = dictSearch ( source[ i ], ADFGVX_ru ).lower ( )
        toCip += [ letter ]

    return ('' if rev else ' ').join ( toCip )

''' Версия для английского алфавита

def combine_cip ( s, rev ):
    source = s.upper ( ).split ( ) if rev else s.upper ( )
    toCip = [ ]

    for i in range ( len ( source ) ):
        letter = ''
        if rev:
            letter = ADFGVX_en [ source[ i ] ]
        else:
            letter = dictSearch ( source[ i ], ADFGVX_en )
        toCip += [ letter ]

    return ('' if rev else ' ').join ( toCip )

'''

# RSA

keyPublic, keyPrivate = keyGen ( )

def rsa ( s, rev ):
    if not rev:
        txt = encrypt ( keyPublic, s )
        for i in range ( len ( txt ) ):
            txt[ i ] = toHex ( txt[ i ] )
        return ' '.join ( txt )
    else:
        txt = s.split ( )
        for i in range ( len ( txt ) ):
            txt[ i ] = fromHex ( txt[ i ] )
        return decrypt ( keyPrivate, txt )