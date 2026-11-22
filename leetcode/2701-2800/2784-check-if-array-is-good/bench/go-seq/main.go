// LeetCode #2784: Check if Array is Good -- the bench in Go: the ★ arm
// over 50000 arrays of 100 numbers, base[99] shuffled and two in three
// with one number changed to one up to 200, all drawn first, then each
// answered 40 times.
package main

import "fmt"

func isGood(nums []int64) bool {
	n := int64(len(nums)) - 1
	if n < 1 {
		return false
	}
	counts := make([]int64, n+1)
	for _, v := range nums {
		if v < 1 || v > n {
			return false
		}
		counts[v]++
	}
	for v := int64(1); v < n; v++ {
		if counts[v] != 1 {
			return false
		}
	}
	return counts[n] == 2
}

var seed int64 = 2784

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func shuffledBase(n int64) []int64 {
	nums := make([]int64, 0, n+1)
	for v := int64(1); v <= n; v++ {
		nums = append(nums, v)
	}
	nums = append(nums, n)
	for i := n; i > 0; i-- {
		j := nextRandom() % (i + 1)
		nums[i], nums[j] = nums[j], nums[i]
	}
	return nums
}

func main() {
	count := 50000
	rounds := 40
	cases := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		nums := shuffledBase(99)
		if nextRandom()%3 != 0 {
			at := nextRandom() % 100
			nums[at] = nextRandom()%200 + 1
		}
		cases = append(cases, nums)
	}
	var good, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, nums := range cases {
			g := isGood(nums)
			var w int64 = 1
			if g {
				good++
				w = 2
			}
			check = (check*31 + w + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 100, %d rounds: %d good, checksum %d\n", count, rounds, good, check)
}
