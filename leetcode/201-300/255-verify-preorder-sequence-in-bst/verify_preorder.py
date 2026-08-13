"""LeetCode 255 - Verify Preorder Sequence in BST. Python oracle.

Mirrors verify_preorder.kara algorithm-for-algorithm: a stack of ancestors whose
right subtree has not been entered, plus a lower bound that only ever rises.

The bound starts at the i64 minimum and the test is STRICT (`x < lower`), so a
genuine i64.MIN in the data is still accepted -- `[i64.MIN, 5]` is in the tests
for that.
"""

I64_MIN = -(2**63)


def verify_preorder(preorder):
    stack = []
    lower = I64_MIN
    for x in preorder:
        if x < lower:
            return False
        while stack and stack[-1] < x:
            lower = stack.pop()
        stack.append(x)
    return True


def main():
    cases = [
        ([5, 2, 1, 3, 6], "[5,2,1,3,6]"),
        ([5, 2, 6, 1, 3], "[5,2,6,1,3]"),
        ([], "[]"),
        ([1], "[1]"),
        ([1, 2], "[1,2]"),
        ([2, 1], "[2,1]"),
        ([2, 3, 1], "[2,3,1]"),
        ([1, 3, 2], "[1,3,2]"),
        ([1, 2, 3, 4, 5], "[1,2,3,4,5]"),
        ([5, 4, 3, 2, 1], "[5,4,3,2,1]"),
        ([10, 5, 1, 7, 40, 50], "[10,5,1,7,40,50]"),
        ([10, 5, 1, 7, 40, 50, 30], "[10,5,1,7,40,50,30]"),
        ([I64_MIN, 5], "[i64.MIN,5]"),
    ]
    for iv, label in cases:
        print(f"{label} -> {str(verify_preorder(iv)).lower()}")


if __name__ == "__main__":
    main()
