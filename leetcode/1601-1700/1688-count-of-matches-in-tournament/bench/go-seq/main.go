// LeetCode #1688: Count of Matches in Tournament -- the bench's Go mirror:
// the ★ arm on 500000 random n up to 10^9, all drawn first, each answered
// 40 times.
package main

import "fmt"

func matches(n int32) int32 {
	teams, played := n, int32(0)
	for teams > 1 {
		played += teams / 2
		teams = (teams + 1) / 2
	}
	return played
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1688

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 500000, 40
	values := make([]int32, count)
	for i := range values {
		hi := nextRandom()
		values[i] = int32((hi*32768+nextRandom())%1000000000 + 1)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, n := range values {
			answer := int64(matches(n))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d values of n, %d rounds: %d matches, checksum %d\n", count, rounds, total, check)
}
