# -*- coding: utf8 -*-
import random
class Bitarray:
    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(size//8+1)

    def set(self, n):
        """ Sets the nth element of the bitarray """
        index = n//8
        position = n % 8
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)

    def get(self, n):
        """ Gets the nth element of the bitarray """
        index = n//8
        position = n % 8
        return (self.bitarray[index] & (1 << (7 - position))) > 0


def BKDRHash(key,k,m):#参数有k、m，返回数组
    seeds=[31,131,1313,13131,131313,1313131,13131313,131313131,1313131313,13131313131]#31 131 1313 13131 131313 etc..
    hash_res = []
    for i in range(k):
        seed=seeds[i]
        hash=0
        for j in range(len(key)):
            hash=(hash*seed)+ord(key[j])
            hash=hash%m
        hash_res.append(hash)
    return hash_res

def test_hash_function(filename):
    some_words=[]
    test_words=[]
    f=open(filename,'r')
    for line in f.readlines():
        for word in line.strip().split(' '):
            flag=random.randint(0,1)
            if(flag):
                if(not word in some_words):
                    some_words.append(word)
            else:
                if(not word in test_words):
                    test_words.append(word)
    n=len(test_words)
    m=2*n#靠近k*ln2;其实m取很大是好的
    k=10
    bitarray_obj = Bitarray(m)
    for key in some_words:
        hash_res=BKDRHash(key,k,m)
        for i in hash_res:
            bitarray_obj.set(i)


    count=0
    right=0
    for key in test_words:
        hash_res=BKDRHash(key,k,m)
        all_same=1
        for i in hash_res:
            if (bitarray_obj.get(i)!=1):
                all_same=0
                break
        if(all_same==1):
            count+=1
            if(key in some_words):
                right+=1

    return right/count



if __name__ == "__main__":
    file="/Users/markdana/Desktop/pg1661.txt"
    print(test_hash_function(file))



