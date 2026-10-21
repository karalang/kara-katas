// Benchmark for #837: New 21 Game -- the ★ arm (forward, with a sliding window).
//
// Mirrors new21_game.kara: p[i] is the chance that Alice's points are ever
// exactly i, the sum over max_pts of the chances of the totals in the last
// max_pts below i at which she still draws, kept in a running window.
package main

import "fmt"

func new21Game(n, k, maxPts int64) float64 {
	if k == 0 || n >= k-1+maxPts {
		return 1.0
	}
	w := float64(maxPts)
	p := make([]float64, n+1)
	p[0] = 1.0
	window := 1.0
	answer := 0.0
	for i := int64(1); i < n+1; i++ {
		p[i] = window / w
		if i < k {
			window += p[i]
		} else {
			answer += p[i]
		}
		gone := i - maxPts
		if gone >= 0 && gone < k {
			window -= p[gone]
		}
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 64 games drawn once, each with n from 5000 to 10^4, k from n / 2 to
	// n, and maxPts large enough that Alice can go past n, so that no game
	// takes the early return. Each round plays the next game.
	count := int64(64)
	rounds := int64(25000)
	seed := int64(837)
	games := make([][3]int64, 0)
	for g := int64(0); g < count; g++ {
		n := 5000 + nextRandom(&seed)%5001
		k := n/2 + nextRandom(&seed)%(n-n/2+1)
		least := n - k + 2
		maxPts := least + nextRandom(&seed)%(10001-least)
		games = append(games, [3]int64{n, k, maxPts})
	}
	sum := 0.0
	for round := int64(0); round < rounds; round++ {
		g := games[round%count]
		sum += new21Game(g[0], g[1], g[2])
	}
	fmt.Printf("%d rounds of %d games: sum %.6f\n", rounds, count, sum)
}
