#!/usr/bin/env python3

import random

random.seed(42)

bases = ["A", "C", "G", "T"]

def replace_char_at(string, pos, char):
    lst = list(string)
    lst[pos] = char
    return "".join(lst)

def other_bases(x):
    assert x in bases
    return [b for b in bases if b != x]

true_seq = "".join(random.choices(bases, k=10))
err1_seqs = [replace_char_at(true_seq, i, b) for i in range(len(true_seq)) for b in other_bases(true_seq[i])]

print(true_seq)
print(*err1_seqs, sep="\n")
