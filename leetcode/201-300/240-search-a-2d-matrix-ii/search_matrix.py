# LeetCode 240 — Search a 2D Matrix II (oracle mirror).
def search_matrix(flat, rows, cols, target):
    if rows == 0 or cols == 0: return False
    r, c = 0, cols - 1
    while r < rows and c >= 0:
        v = flat[r * cols + c]
        if v == target: return True
        elif v > target: c -= 1
        else: r += 1
    return False
def report(flat, rows, cols, t): print("true" if search_matrix(flat, rows, cols, t) else "false")
m = [1,4,7,11,15, 2,5,8,12,19, 3,6,9,16,22, 10,13,14,17,24, 18,21,23,26,30]
for t in (5, 20, 1, 30, 31, 0, 14): report(m, 5, 5, t)
