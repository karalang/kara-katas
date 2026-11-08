// LeetCode #1510: Stone Game IV -- the bench: 40 piles of 50000 to 100000
// stones, each answered by the ★ arm.
package main

import "fmt"

func winnerSquareGame(n int64) bool {
	wins := make([]bool, n+1)
	for pile := int64(1); pile <= n; pile++ {
		for k := int64(1); k*k <= pile; k++ {
			if !wins[pile-k*k] {
				wins[pile] = true
				break
			}
		}
	}
	return wins[n]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1510)
	var wins, check int64
	for i := 0; i < 40; i++ {
		hi := nextRandom(&seed) * 32768
		n := 50000 + (hi+nextRandom(&seed))%50001
		w := winnerSquareGame(n)
		var v int64
		if w {
			wins++
			v = n
		}
		check = (check*31 + v + 1) % 1000000007
	}
	fmt.Printf("40 piles of 50000 to 100000 stones: Alice wins %d, checksum %d\n", wins, check)
}
