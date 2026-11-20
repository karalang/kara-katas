// LeetCode #1690: Stone Game VII -- the bench's Go mirror: the ★ arm on 40
// random rows of 1000 stones, all drawn first, each answered 4 times.
package main

import "fmt"

func stoneGame(stones []int32) int32 {
	n := len(stones)
	prefix := make([]int32, n+1)
	for i := 0; i < n; i++ {
		prefix[i+1] = prefix[i] + stones[i]
	}
	best := make([]int32, n)
	for i := n - 1; i >= 0; i-- {
		for j := i + 1; j < n; j++ {
			takeLeft := prefix[j+1] - prefix[i+1] - best[j]
			takeRight := prefix[j] - prefix[i] - best[j-1]
			best[j] = max(takeLeft, takeRight)
		}
	}
	return best[n-1]
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1690

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, size, rounds = 40, 1000, 4
	rows := make([][]int32, count)
	for c := range rows {
		rows[c] = make([]int32, size)
		for i := range rows[c] {
			rows[c][i] = int32(nextRandom()%1000 + 1)
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, stones := range rows {
			answer := int64(stoneGame(stones))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d rows of %d stones, %d rounds: answers sum to %d, checksum %d\n", count, size, rounds, total, check)
}
