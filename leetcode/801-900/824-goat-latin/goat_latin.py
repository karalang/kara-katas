# LeetCode 824 — Goat Latin, by split and a growing suffix.
#
# Mirrors goat_latin.kara: split the sentence at spaces, keep a first
# vowel and move a first consonant to the end of its word, then add "ma"
# and a run of a's one longer than the word before's.

def to_goat_latin(sentence):
    answer = []
    tail = ""
    for word in sentence.split(" "):
        tail += "a"
        first = word[0]
        if first in "aeiouAEIOU":
            w = word
        else:
            w = word[1:] + first
        answer.append(w + "ma" + tail)
    return " ".join(answer)

seed = 0
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def show(s):
    print(f'"{s}" -> "{to_goat_latin(s)}"')

def random_sentence(words, longest):
    letters = "aeiouAEIOUbcdfgBCDFGxyzXYZ"
    out = []
    for w in range(words):
        length = 1 + next_random() % longest
        out.append("".join(letters[next_random() % 26] for _ in range(length)))
    return " ".join(out)

show("I speak Goat Latin")
show("The quick brown fox jumped over the lazy dog")
show("a")
show("b")
show("A B")
show("Each word consists of lowercase and uppercase letters only")
show("aaa bbb ccc")
show("U I O E A")
seed = 824
largest = random_sentence(75, 1)
goat = to_goat_latin(largest)
print(f"75 one-letter words: {len(largest)} characters -> {len(goat)}")
total = 0
check = 0
for _ in range(300):
    words = 1 + next_random() % 12
    s = random_sentence(words, 8)
    out = to_goat_latin(s)
    total += len(out)
    for b in out.encode():
        check = (check * 131 + b) % 1000000007
print(f"300 random sentences: total {total}, checksum {check}")
