// LeetCode #1753: Maximum Score From Removing Stones -- the bench
// (stones.kara in Go): a closed form.
package main

import "fmt"

func maximumScore(a, b, c int32) int32 {
	total := a + b + c
	largest := max(a, max(b, c))
	return min(total/2, total-largest)
}

var seed int64 = 1753

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	const count, rounds = 2000000, 5
	piles := make([][3]int32, count)
	for i := range piles {
		for j := 0; j < 3; j++ {
			piles[i][j] = int32(wide()%100000 + 1)
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range piles {
			answer := int64(maximumScore(p[0], p[1], p[2]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d sets of piles, %d rounds: scores add to %d, checksum %d\n", count, rounds, sum, check)
}
