__author__ = 'keithd'

# A subset of prims1.py used for projects in TDT-4113

from inspect import isfunction # Need this to test whether something is a function!

# The reduce function was removed in Python 3.0, so just use this handmade version.  Same as a curry.
def kd_reduce(func,seq):
    res = seq[0]
    for item in seq[1:]:
        res = func(res,item)
    return res

def group(L,size):
    groups = []; lmax = len(L); loc = 0
    while loc < lmax:
        groups.append(L[loc:min(loc+size,lmax)])
        loc += size
    return groups

# Returns n versions of either a number or string, or the result of calling the same function n times.
def n_of(count, item):
    if isfunction(item):
        return [item() for i in range(count)]
    else:
        return [item for i in range(count)]

# Calculate the frequency of occurrence of every character in a file, whose pathname is the argument 'fid'.
def calc_char_freqs(fid,lc=True):
    "Create a dictionary with pairs (char : freq) based on the entire file"
    return gen_freqs(all_chars_from_file(fid,lc=lc))

def gen_freqs(items):
    " Creates a dictionary of pairs (item : frequency)"
    fc = {}
    for item in items:
        if item in fc.keys():
            fc[item] = fc[item] + 1
        else:
            fc[item] = 1
    size = len(items)
    for key in fc.keys():
        fc[key] = fc[key]/size
    return fc

def all_chars_from_file(fid,lc=True):
    if lc: return lowercase_chars_from_file(fid)
    else: return strings_explode(load_file_lines(fid))

def lowercase_chars_from_file(fid):
    return [c.lower() for c in strings_explode(load_file_lines(fid))]

def read_message_from_file(fid,lc=True):
    s = big_string_from_file(fid)
    return s.lower() if lc else s

def big_string_from_file(fid):
    return merge_strings(load_file_lines(fid))

# Loads in all lines of a file
def load_file_lines(fid):
    return [line.rstrip() for line in open(fid, 'r').readlines()]
    # rstrip strips the newline character.

def string_explode(s):
    "Generate a list of characters (singleton strings) from a string"
    items = []
    for i in range(len(s)):
        items.append(s[i])
    return items

def strings_explode(strings):
    "Returns one huge list of all the exploded strings"
    items = []
    for s in strings:
        items.extend(string_explode(s))
    return items

def n_strings(count,base,gap=''):
    " Create n copies of the same string, with the string 'gap' between each copy"
    return merge_strings(n_of(count,base),gap=gap)

def merge_strings(strings, gap=' '):
        return kd_reduce((lambda x, y: x + gap + y), strings)

# *** Dictionary operations ***

# Convert the values to keys, and keys to values.  This assumes that there are no identical values.  If there are,
# then some of the keys (turned to values) in d2 will get overwritten.

def invert_dictionary(d):
    d2 = {}
    for k,v in zip(d.keys(),d.values()):
        d2[v] = k
    return d2

#  ******* Bit - Integer Conversions *******
#  In all of these routines, the LEAST significant bits come first in the bit lists and bit strings.  To get
#  the most significant bits first, use the "least_first=False" option.

def bits_to_integer (bits,least_first=True):
    if least_first:
        bits2 = bits
    else:
        bits2 = bits.copy()
        bits2.reverse()
    sum = 0
    for b in range(len(bits2) - 1, -1, -1):
        sum = sum * 2 + bits2[b]
    return sum

def integer_to_bits(int, min_size=False,least_first=True):
    remains = int
    bits = []
    while remains > 0:
        bits.append(remains % 2)
        remains = remains // 2
    if min_size: # pad with zeros
        for i in range(min_size - len(bits)): bits.append(0)
    if not(least_first): bits.reverse()
    return bits

def integer_to_bitstring(int, min_size=False,least_first=True):
    return list_to_string(integer_to_bits(int,min_size,least_first=least_first))

def bitstring_to_integer (bits,least_first=True):
    return bits_to_integer([int(bs) for bs in string_explode(bits)],least_first=least_first)

# ********** string - ascii conversions ******

def string_to_ascii(str): return [ord(x) for x in str]
def ascii_to_string(ascii_list): return merge_strings([chr(c) for c in ascii_list], gap='')

def string_to_ascii_bits(str):
    return merge_strings([integer_to_bitstring(i,8,least_first=False) for i in string_to_ascii(str)],gap='')

def ascii_bits_to_string(bitstring):
    return merge_strings([chr(bitstring_to_integer(s,least_first=False)) for s in group(bitstring,8)],gap='')

def list_to_string(L,gap=None):
    if L:
        s = str(L[0])
        for item in L[1:]:
            if gap: s += gap
            s += str(item)
    return s

