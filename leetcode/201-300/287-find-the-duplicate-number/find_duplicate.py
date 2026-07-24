# LeetCode 287 — Find the Duplicate Number (oracle mirror).
def find_duplicate(nums):
    slow = nums[0]; fast = nums[0]
    slow = nums[slow]; fast = nums[nums[fast]]
    while slow != fast:
        slow = nums[slow]; fast = nums[nums[fast]]
    finder = nums[0]
    while finder != slow:
        finder = nums[finder]; slow = nums[slow]
    return finder
for arr in ([1,3,4,2,2], [3,1,3,4,2], [1,1], [2,2,2,2,2], [1,4,6,7,2,3,5,6]):
    print(find_duplicate(arr))
