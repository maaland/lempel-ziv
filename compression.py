__author__ = 'Marius'

from kdprims import read_message_from_file, calc_char_freqs
from abc import abstractmethod
import PythonLabs.BitLab as btl




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
















