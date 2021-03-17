import math
import numpy as np
from random import randint


def PrimeGen( n = 10000 ):
    sieve = np.ones ( n//2, dtype = np.bool )
    for i in range( 3, int ( n**0.5 ) + 1, 2 ):
        if sieve[ i//2 ]:
            sieve[ i * i//2::i ] = False
    return np.r_[ 2, 2 * np.nonzero ( sieve )[ 0 ][ 1:: ] + 1 ]

def lcm( p, q ):
    return ( p * q ) / math.gcd ( p,q )

def extended_gcd ( aa, bb ):
    lastremainder, remainder = abs ( aa ), abs ( bb )
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, ( quotient, remainder) = remainder, divmod ( lastremainder, remainder )
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * ( -1 if aa < 0 else 1 ), lasty * ( -1 if bb < 0 else 1 )

def modinv ( a, m ):
    g, x, y = extended_gcd ( a, m )
    if g !=  1:
        raise ValueError
    return x % m

def mult_inverse ( e, lamda ):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_lamda = lamda 
    
    while e > 0:
        temp1 = temp_lamda / e
        temp2 = temp_lamda - temp1 * e
        temp_lamda = e
        e = temp2
        
        x = x2- temp1 * x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_lamda ==  1:
        return d + lamda

def keyGen ( ):

    i_p = randint( 0,20 )
    i_q = randint( 0,20 )
    while i_p == i_q:
        continue
    primes = PrimeGen ( 100 )
    p = primes[ i_p ]
    q = primes[ i_q ]

    n = p * q

    lamda_n = int ( lcm ( p - 1, q - 1 ) )
    e = randint( 1, lamda_n )

    while math.gcd ( e, lamda_n ) != 1:
        e = randint ( 1, lamda_n )

    d = modinv( e, lamda_n )

    return ( ( e, n ), ( d, n ) )

def encrypt( pk, message ):

    key, n = pk

    cipher = [ ( ord ( char ) ** key ) % n for char in message ]

    return cipher

def decrypt( pk, cipher ):

    key, n = pk

    message = [ chr( ( char ** key ) % n ) for char in cipher ]

    return ''.join ( message )