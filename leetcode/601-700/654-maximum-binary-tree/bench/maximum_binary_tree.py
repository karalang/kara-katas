# Benchmark for #654: a stack of the right spine, as the Kara ★ arm.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def construct_maximum_binary_tree(nums):
    stack = []
    for x in nums:
        node = TreeNode(x)
        while stack and stack[-1].val < x:
            node.left = stack.pop()
        if stack:
            stack[-1].right = node
        stack.append(node)
    return stack[0] if stack else None


seed = 654


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    inputs = 8
    rounds = 100
    n = 200000
    lists = []
    for _ in range(inputs):
        nums = list(range(n))
        i = n - 1
        while i > 0:
            hi = next_random()
            j = (hi * 32768 + next_random()) % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
            i -= 1
        lists.append(nums)
    checksum = 0
    for r in range(rounds):
        root = construct_maximum_binary_tree(lists[(r * 3) % inputs])
        left = 0
        at = root
        while at is not None:
            left += 1
            at = at.left
        right = 0
        at = root
        while at is not None:
            right += 1
            at = at.right
        checksum = (checksum * 31 + left * 1000 + right) % 1000000007
    print(f"{inputs} orders of {n}, {rounds} rounds: checksum {checksum}")


main()
