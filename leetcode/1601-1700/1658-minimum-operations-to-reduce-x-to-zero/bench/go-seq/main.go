// LeetCode #1658: Minimum Operations to Reduce X to Zero -- the bench's Go
// mirror: the ★ arm on 1000 random arrays of 100000 numbers from 1 to
// 10000, each x a random prefix plus a random suffix of its array, all
// drawn first.
package main

import "fmt"

func minOperations(nums []int32, x int32) int32 {
	var total int64
	for _, v := range nums {
		total += int64(v)
	}
	target := total - int64(x)
	if target < 0 {
		return -1
	}
	n := int64(len(nums))
	var longest int64 = -1
	var sum, left int64
	for right := int64(0); right < n; right++ {
		sum += int64(nums[right])
		for sum > target {
			sum -= int64(nums[left])
			left++
		}
		if sum == target {
			longest = max(longest, right-left+1)
		}
	}
	if longest < 0 {
		return -1
	}
	return int32(n - longest)
}

var seed int64 = 1658

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	type problem struct {
		nums []int32
		x    int32
	}
	problems := make([]problem, 0, 1000)
	for p := 0; p < 1000; p++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32(nextRandom()%10000 + 1)
		}
		left := nextRandom() % 1000
		right := nextRandom() % 1000
		var x int64
		for i := int64(0); i < left; i++ {
			x += int64(nums[i])
		}
		for i := n - right; i < n; i++ {
			x += int64(nums[i])
		}
		problems = append(problems, problem{nums, int32(max(x, 1))})
	}
	var check, total int64
	for _, p := range problems {
		answer := int64(minOperations(p.nums, p.x))
		total += answer
		check = (check*31 + answer + 2) % 1000000007
	}
	fmt.Printf("1000 arrays of 100000 numbers: operations sum to %d, checksum %d\n", total, check)
}
