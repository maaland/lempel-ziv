__author__ = 'Marius'

from kdprims import read_message_from_file, calc_char_freqs
from abc import abstractmethod
import PythonLabs.BitLab as btl
import math



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
            binnumber = '{0:08}'.format(number)
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
            intnumber = int(binnumber, 10)
            d = d + chr(intnumber)
        return d

    def encode_decode_test(self, message):
        print(message)
        e = self.encode(message)
        d = self.decode(e)
        print(e)
        print(d)
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
        return btl.huffman_encode(msg, self.tree)


    def decode(self, encoded_msg):
        return btl.huffman_decode(encoded_msg, self.tree)

    def encode_decode_test(self, message):
        print(message)
        e = self.encode(message)
        d = self.decode(e)
        print(e)
        print(d)
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


class LempelZiv(Coder):


    def encode(self, source):
        slen = len(source)
        target = []
        target[0] = source[0]
        LT = { "" : 0 , source[0] : 1}
        size = 2
        currloc = 1
        while currloc < slen:
            [oldseg, newbit] = self.findNextSegment(source, currloc, LT)
            bitlen = [math.log(size, 2)]
            index = LT.get(oldseg)
            index_bits = self.IntegerToBits(index, bitlen)
            target.append(index_bits + newbit)
            LT[oldseg + newbit] = index + 1
            currloc = currloc + len(oldseg) + 1
            size = size +1
        return target

    def decode(self, target):
        tlen = len(target)
        source = target[0]
        LT = ["", target[0]]
        loc = 1
        size = 2
        while loc < tlen:
            bitlen = [math.log(size, 2)]
            index = self.BitsToInteger(target[loc : loc + bitlen])
            seg = LT[index]
            if loc + bitlen < tlen:
                seg = seg + target[loc + bitlen]
                size = size + 1
                LT[size] = seg
                loc = loc + 1
            source = source + seg
            loc = loc + 1
        return source

    







    def IntegerToBits(self, index, bitlen):
        format = '0' + str(bitlen)
        return '{0:format}'.format(index)

    def BitsToInteger(self, str):
        return int(str, 10)


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






