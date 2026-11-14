// LeetCode #2139: Minimum Moves to Reach Target Score -- the benchmark,
// the same algorithm as moves.kara.
package main

import "fmt"

func minMoves(target, maxDoubles int64) int64 {
	doubles, moves := maxDoubles, int64(0)
	for target > 1 && doubles > 0 {
		if target%2 == 1 {
			target--
		} else {
			target /= 2
			doubles--
		}
		moves++
	}
	return moves + target - 1
}

var seed int64 = 2139

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	targets := make([]int64, 1000)
	for i := range targets {
		hi := nextRandom()
		targets[i] = (hi*32768+nextRandom())%1000000000 + 1
	}
	total, check := int64(0), int64(0)
	for r := int64(0); r < 4000; r++ {
		for i := 0; i < 1000; i++ {
			moves := minMoves(targets[i]+r, r%40)
			total += moves
			check = (check*31 + moves) % 1000000007
		}
	}
	fmt.Printf("4000000 solves: %d moves in all, checksum %d\n", total, check)
}
