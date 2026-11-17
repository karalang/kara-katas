// LeetCode #2220: Minimum Bit Flips to Convert Number -- bench mirror of
// flips.kara: the 1 bits of start ^ goal, counted by clearing the lowest
// with x & (x - 1).
package main

import "fmt"

func minBitFlips(start, goal int64) int64 {
	differ := start ^ goal
	var flips int64
	for differ != 0 {
		differ &= differ - 1
		flips++
	}
	return flips
}

var seed int64 = 2220

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	// 10^5 pairs up to 10^9
	starts := make([]int64, 100000)
	goals := make([]int64, 100000)
	for i := range starts {
		starts[i] = wideRandom() % 1000000001
		goals[i] = wideRandom() % 1000000001
	}
	var check int64
	for r := 0; r < 50; r++ {
		// punch: one goal is drawn again before each round
		goals[r*1999] = wideRandom() % 1000000001
		var total int64
		for i := range starts {
			total += minBitFlips(starts[i], goals[i])
		}
		check = (check*31 + total) % 1000000007
	}
	fmt.Printf("10^5 pairs, 50 punches: checksum %d\n", check)
}
