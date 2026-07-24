# LeetCode 274 — H-Index (oracle mirror).
def h_index(cit):
    v = sorted(cit); n = len(v)
    for j in range(n):
        if v[j] >= n - j: return n - j
    return 0
for arr in ([3,0,6,1,5], [1,3,1], [0], [100], [4,4,4,4], [10,8,5,4,3,0]):
    print(h_index(arr))
