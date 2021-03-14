import copy
import string
import math
import numpy as np

def minor(A, i, j):
    M = copy.deepcopy(A)
    del M[i]
    for i in range(len(A[0]) - 1):
        del M[i][j]
    return M

#Создание матрицы
def gener_matrix(text,slovar):
    matrix_str = math.ceil(len(text)/3)
    text_matrix=[[9 for j in range(3)] for i in range(matrix_str)]
    tmp=[]
    for i in range(len(text)):
        tmp.append(slovar[text[i]])
    c=0
    for i in range(matrix_str):
        for j in range(3):
            text_matrix[i][j]=tmp[c]
            c+=1
    return text_matrix

#Замена 
def gener_out(matrix, slovar):
    matrix_str=len(matrix)
    matrix_stol=len(matrix[0])
    plaintext=''
    for i in range(matrix_str):
        for j in range(matrix_stol):
            if matrix[i][j] in slovar:
                plaintext+=slovar[matrix[i][j]]
    return plaintext


#Расширенный алоритм Евклида
def REvclid(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return (x, y, a)


def enncryption(plaintext, key):
    tmp = np.dot(plaintext,key)%37
    ciphertext = gener_out(tmp, rev_dict)
    return ciphertext
    return tmp



def decryption(ciphertext, key):
    matrix = gener_matrix(ciphertext, slovar)
    tmp = np.zeros((3,3))
    deter = round((np.linalg.det(key)))
    x = REvclid(deter,37)[0]
    rev_det = round(x % 37)
    for i in range(len(key)):
        for j in range(len(key[i])):
            t = minor(key, i, j)
            if (i+j) % 2 == 1:
                tmp[i][j] = -1 * np.linalg.det(t)
            else:
                tmp[i][j] = 1 * np.linalg.det(t)
    tmp = (np.dot(matrix, np.transpose((np.array(tmp)%37*rev_det)%37)))
    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            tmp[i][j] = round(tmp[i][j])%37
            if tmp[i][j]<0:
                tmp[i][j]=tmp[i][j]+37
    text = gener_out(tmp, rev_dict)
    return text

slovar={'а':0,'б':1,'в':2,'г':3,'д':4,'е':5,'ё':6,'ж':7,'з':8,'и':9,'й':10,
        'к':11,'л':12,'м':13,'н':14,'о':15,'п':16,'р':17,'с':18,'т':19,'у':20,
        'ф':21,'х':22,'ц':23,'ч':24,'ш':25,'щ':26,'ь':27,'ы':28,'ъ':29,'э':30,
        'ю':31,'я':32,'!':33,'@':34,':':35,' ':36}    
rev_dict = {a:b for b,a in slovar.items()}

def hill_cip ( text, rev ):
    key = 'мой  ключ'
    spec_key = ' '
    toCip = text
    l = len ( text )
    lk = len ( key )
    sq = int ( math.sqrt ( lk ) )

    while ( l % sq != 0 ):
        l += 1
    
    toCip += spec_key * ( l - len ( text ) )

    matrix_t = gener_matrix ( toCip, slovar )
    matrix_k = gener_matrix ( key, slovar )

    return decryption ( toCip, matrix_k ).rstrip ( ) if rev else enncryption ( matrix_t, matrix_k )