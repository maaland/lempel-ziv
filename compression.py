__author__ = 'Marius'

from kdprims import read_message_from_file, calc_char_freqs
from abc import abstractmethod
import PythonLabs.BitLab as btl
import math
import os



class Coder:



    def gen_message_from_file(self, filepath):
        message = read_message_from_file(filepath)
        return message

    @abstractmethod
    def encode_decode_test(self, message):
      pass



class Asciicoder(Coder):




    def encode(self, str):
        e = ""
        for c in str:
            number = ord(c)
            binnumber = bin(number)[2:].zfill(8)
            e = e + binnumber
        return e

    def decode(self, bits):
        d = ""
        bitlist = list(bits)

        while bitlist:
            binnumber = ""
            i = 0
            while i < 8:
                binnumber = binnumber + bitlist.pop(0)
                i = i+1
            intnumber = int(binnumber, 2)
            d = d + chr(intnumber)
        return d

    def encode_decode_test(self, message):
        print("Message: " + message)
        e = self.encode(message)
        d = self.decode(e)
        print("Encoded message: " + e)
        print("Decoded message: "+ d)
        if d == message:
            print ("The original and decoded messages are equal")
        else:
            print ("The original and decoded messages are not equal ")
        L = len(message)
        E = len(e)
        factor = (1- (E/(L*8)))
        print("M length: " + str(L))
        print("E length: " + str(E))
        print("D length: " + str(len(d)))
        print("Compression fraction: " + str(factor) )  #binary-binary version. L*8 for text-binary



class Huffcoder(Coder):

    def __init__(self):
        self.frequencies = {}
        self.bits = ""

    def prepare(self, fid):
        self.frequencies = calc_char_freqs(fid, lc = True)



    def build_tree(self, freqs):
        pq = btl.init_queue(freqs)
        while len(pq) > 1:
            n1 = pq.pop()
            n2 = pq.pop()
            pq.insert(btl.Node(n1, n2))
        self.tree = pq[0]


    def encode(self, msg):
        self.prepare('corpus1.txt')
        self.build_tree(self.frequencies)
        return btl.huffman_encode(msg, self.tree)


    def decode(self, encoded_msg):
        return btl.huffman_decode(encoded_msg, self.tree)

    def encode_decode_test(self, message):
        print("Message: " + message)
        e = self.encode(message)
        d = self.decode(e)
        print("Encoded message: " + e.__repr__())
        print("Decoded message: "+ d.__repr__())
        print(e.__repr__())
        print(d.__repr__())
        if d == message:
            print ("The original and decoded messages are equal")
        else:
            print ("The original and decoded messages are not equal ")
        L = len(message)
        E = len(e.__repr__())
        factor = (1- (E/(L*8)))
        print("M length: " + str(L))
        print("E length: " + str(E))
        print("D length: " + str(len(d.__repr__())))
        print("Compression fraction: " + str(factor) )


class LempelZiv(Coder):


    def encode(self, source):
        slen = len(source)
        target = []
        target.append(source[0])
        LT = { "" : 0 , source[0] : 1}
        size = 2
        currloc = 1
        while currloc < slen:
            [oldseg, newbit] = self.findNextSegment(source, currloc, LT)
            bitlen = math.ceil(math.log2(size))
            index = LT.get(oldseg)
            index_bits = self.IntegerToBits(index, bitlen)
            target.append(index_bits + newbit)
            LT[oldseg + newbit] = size
            currloc = currloc + len(oldseg) + 1
            size = size +1
        return "".join(target)

    def decode(self, target):
        tlen = len(target)
        source = target[0]
        LT = ["", target[0]]
        loc = 1
        size = 2
        while loc < tlen:
            bitlen = int(math.log(size, 2))
            index = self.BitsToInteger("".join(target[loc : loc + bitlen]))
            seg = LT[index]
            if loc + bitlen < tlen:
                seg = seg + target[loc + bitlen]
                size = size + 1
                LT.append(seg)
                loc = loc + 1
            source = source + seg
            loc = loc + 1
        return source

    def encode_decode_test(self, message):
        print("Message: " + message)
        e = self.encode(message)
        d = self.decode(e)
        print("Encoded message: "+ e)
        print("Decoded message: " +d)
        if d == message:
            print ("The original and decoded messages are equal")
        else:
            print ("The original and decoded messages are not equal ")
        L = len(message)
        E = len(e)
        factor = (1- (E/(L*8)))
        print("M length: " + str(L))
        print("E length: " + str(E))
        print("D length: " + str(len(d)))
        print("Compression fraction: " + str(factor) )









    def IntegerToBits(self, index, bitlen):
        return bin(index)[2:].zfill(bitlen)

    def BitsToInteger(self, str):
        return int(str, 2)


    def findNextSegment(self, source, loc, table):
        seg = ""
        oldseg = ""
        newbit = ""
        while table.get(seg, -1) >= 0 :
            if (loc >= len(source)):
                return [seg, ""]
            newbit = source[loc]
            loc = loc +1
            oldseg = seg
            seg = seg + newbit
        return [oldseg, newbit]



def Ascii_test(msg='Hello World', filepath=False, lz_flag=False):
    if filepath == False and msg != None:
        message = msg
    elif filepath != False:
        message = Coder.gen_message_from_file(filepath)
    else:
        message = "Hello World"
    if lz_flag == True:
        coder1 = Asciicoder()
        coder2 = LempelZiv()
        coder1.encode_decode_test(message)
        coder2.encode_decode_test(coder1.encode(message))
    else:
        coder1 = Asciicoder()
        coder1.encode_decode_test(message)


def Huff_test(msg='Hello World', filepath=False, lz_flag=False):
    if filepath == False and msg != None:
        message = msg
    elif filepath != False:
        message = Coder.gen_message_from_file(filepath)
    else:
        message = "Hello World"
    if lz_flag == True:
        coder1 = Huffcoder()
        coder2 = LempelZiv()
        coder1.encode_decode_test(message)
        coder2.encode_decode_test(coder1.encode(message).__repr__())
    else:
        coder1 = Asciicoder()
        coder1.encode_decode_test(message)

def LZ_test(msg='00000000000000000000', filepath=False):
    pass


#Huff_test("abba", False, True)
lz = LempelZiv()
e = lz.encode('101000000010001')
print (e)
print (lz.decode(e))



