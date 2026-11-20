// LeetCode #1262 bench, in Go: the ★ arm (the best sum with each remainder
// modulo 3, in a [3]int64 copied before each number) on 100 random lists of
// 4 * 10^4 numbers from 1 to 10^4 built once, 30 rounds; every answer folded
// into a checksum.
package main

import "fmt"

func maxSumDivThree(nums []int64) int64 {
	// -1 marks a remainder no sum has reached yet.
	best := [3]int64{0, -1, -1}
	for _, x := range nums {
		before := best
		for r := 0; r < 3; r++ {
			if before[r] >= 0 {
				sum := before[r] + x
				if sum > best[sum%3] {
					best[sum%3] = sum
				}
			}
		}
	}
	return best[0]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1262)
	lists := make([][]int64, 100)
	for l := range lists {
		lists[l] = make([]int64, 40000)
		for i := range lists[l] {
			lists[l][i] = nextRandom(&seed)%10000 + 1
		}
	}
	check := int64(0)
	for round := int64(0); round < 30; round++ {
		for l := 0; l < 100; l++ {
			best := maxSumDivThree(lists[l])
			check = (check*131 + best + round) % 1000000007
		}
	}
	fmt.Printf("30 rounds of 100 lists of 40000: checksum %d\n", check)
}
