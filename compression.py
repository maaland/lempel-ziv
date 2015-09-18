__author__ = 'Marius'

from kdprims import read_message_from_file



class Coder:




    def gen_message_from_file(self, filepath):
        message = read_message_from_file(filepath)
        return message


    def encode_decode_test(self, message):
        print(message)
        # e = encode(message)
        # d = decode(message)
        #print (e)
        #print (d)
        '''if d == message:
            print (The original and decoded messages are equal)
        else:
            print(The original and decoded messages are not equal)'''
        L = len(message)
        print ('M length: ' + L)
        ''' print ('E length: ' + len(e))
        print ('D length: ' + len(d))'''
        #print ('Compression fraction: '1- (len(e))/L)   binary-binary version. L*8 for text-binary








