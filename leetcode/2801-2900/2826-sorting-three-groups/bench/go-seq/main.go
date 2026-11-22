// LeetCode #2826: Sorting Three Groups -- the bench's Go mirror of the ★
// arm: a three-state table of the most numbers kept so far ending at a
// value at most v.
package main

import "fmt"

func minimumOperations(nums []int64) int64 {
	var best [3]int64
	for _, x := range nums {
		v := x - 1
		best[v]++
		for w := v + 1; w < 3; w++ {
			best[w] = max(best[w], best[v])
		}
	}
	return int64(len(nums)) - best[2]
}

var seed int64 = 2826

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 200000, 5
	cases := make([][]int64, count)
	for c := range cases {
		cases[c] = make([]int64, 100)
		for i := range cases[c] {
			cases[c][i] = nextRandom()%3 + 1
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, nums := range cases {
			a := minimumOperations(nums)
			total += a
			check = (check*31 + a + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 100, %d rounds: %d removals, checksum %d\n", count, rounds, total, check)
}
