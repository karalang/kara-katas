// LeetCode #2770: Maximum Number of Jumps to Reach the Last Index -- the
// bench in Go: the ★ arm over 40 arrays of 1000 numbers, all drawn
// first, then each answered 5 times.
package main

import "fmt"

func maximumJumps(nums []int64, target int64) int64 {
	n := len(nums)
	most := make([]int64, n)
	for i := range most {
		most[i] = -1
	}
	most[0] = 0
	for j := 1; j < n; j++ {
		for i := 0; i < j; i++ {
			d := nums[j] - nums[i]
			if d < 0 {
				d = -d
			}
			if most[i] >= 0 && d <= target {
				most[j] = max(most[j], most[i]+1)
			}
		}
	}
	return most[n-1]
}

var seed int64 = 2770

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	b := nextRandom()
	return (a*32768+b)*32768 + nextRandom()
}

func main() {
	count := 40
	rounds := 5
	cases := make([][]int64, count)
	targets := make([]int64, count)
	for c := 0; c < count; c++ {
		cases[c] = make([]int64, 1000)
		for i := range cases[c] {
			cases[c][i] = wide()%2000000001 - 1000000000
		}
		targets[c] = wide() % 2000000001
	}
	var reached, total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := maximumJumps(cases[c], targets[c])
			if a >= 0 {
				reached++
				total += a
			}
			check = (check*31 + a + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 1000, %d rounds: %d reached, jumps sum to %d, checksum %d\n", count, rounds, reached, total, check)
}
