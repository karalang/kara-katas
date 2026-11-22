// LeetCode #2769: Find the Maximum Achievable Number -- the bench in Go:
// the ★ arm over 10^6 random pairs, all drawn first, then each answered
// 50 times into a running checksum.
package main

import "fmt"

func theMaximumAchievableX(num, t int64) int64 {
	return num + 2*t
}

var seed int64 = 2769

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 1000000
	rounds := 50
	nums := make([]int64, count)
	ts := make([]int64, count)
	for i := 0; i < count; i++ {
		nums[i] = nextRandom()%50 + 1
		ts[i] = nextRandom()%50 + 1
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for i := 0; i < count; i++ {
			x := theMaximumAchievableX(nums[i], ts[i])
			total += x
			check = (check*31 + x + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs, %d rounds: answers sum to %d, checksum %d\n", count, rounds, total, check)
}
