// LeetCode #1049: Last Stone Weight II -- Go mirror of
// bench/last_stone.kara.
package main

import "fmt"

var seed int64 = 1049

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func lastStoneWeightII(stones []int64) int64 {
	var total int64
	for _, s := range stones {
		total += s
	}
	half := total / 2
	made := make([]bool, half+1)
	made[0] = true
	for _, s := range stones {
		for t := half; t >= s; t-- {
			if made[t-s] {
				made[t] = true
			}
		}
	}
	best := half
	for !made[best] {
		best--
	}
	return total - 2*best
}

func main() {
	lists, count, rounds := 1000, 30, 10
	all := make([][]int64, lists)
	for l := range all {
		all[l] = make([]int64, count)
		for i := range all[l] {
			all[l][i] = nextRandom()%100 + 1
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, stones := range all {
			answer := lastStoneWeightII(stones)
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("%d lists of %d stones, %d rounds: total %d, checksum %d\n", lists, count, rounds, total, check)
}
