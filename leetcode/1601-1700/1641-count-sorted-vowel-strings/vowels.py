# LeetCode #1641: Count Sorted Vowel Strings -- the Python mirror of the ★
# arm: how many sorted strings end in each vowel, carried forward a letter
# at a time by running sums.


def count_vowel_strings(n):
    ending = [1] * 5
    for _ in range(1, n):
        for v in range(1, 5):
            ending[v] += ending[v - 1]
    return sum(ending)


# ---- the harness: the same as every arm's ---------------------------------

print(count_vowel_strings(1))
print(count_vowel_strings(2))
print(count_vowel_strings(33))
check = 0
total = 0
for n in range(1, 51):
    count = count_vowel_strings(n)
    total += count
    check = (check * 31 + count) % 1000000007
print(f"n from 1 to 50: counts sum to {total}, checksum {check}")
print(count_vowel_strings(50))
