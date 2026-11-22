// LeetCode #2786: Visit Array Positions to Maximize Score -- the bench in
// Go: the ★ arm over 20 arrays of 10^5 numbers up to 10^6 with x up to
// 10^6, all drawn first, then each answered 100 times.
package main

import "fmt"

func maxScore(nums []int64, x int64) int64 {
	var unreached int64 = -1000000000000000
	best := [2]int64{unreached, unreached}
	best[nums[0]%2] = nums[0]
	for _, v := range nums[1:] {
		p := v % 2
		best[p] = max(best[p], best[1-p]-x) + v
	}
	return max(best[0], best[1])
}

var seed int64 = 2786

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count := 20
	rounds := 100
	cases := make([][]int64, count)
	xs := make([]int64, count)
	for c := 0; c < count; c++ {
		cases[c] = make([]int64, 100000)
		for i := range cases[c] {
			cases[c][i] = wide()%1000000 + 1
		}
		xs[c] = wide()%1000000 + 1
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := maxScore(cases[c], xs[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 10^5, %d rounds: scores sum to %d, checksum %d\n", count, rounds, total, check)
}
