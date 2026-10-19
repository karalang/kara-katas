// LeetCode 789 — Escape The Ghosts: the bench, in Go.
// Mirrors escape_ghosts.kara: every ghost's distance to the target
// against yours, stopping at the first that is no farther.
package main

import "fmt"

func abs(v int64) int64 {
	if v < 0 {
		return -v
	}
	return v
}

func escapeGhosts(ghosts [][2]int64, target [2]int64) bool {
	mine := abs(target[0]) + abs(target[1])
	for _, g := range ghosts {
		if abs(g[0]-target[0])+abs(g[1]-target[1]) <= mine {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(789)
	boards := make([][][2]int64, 0, 64)
	for b := 0; b < 64; b++ {
		ghosts := make([][2]int64, 0, 100)
		for i := 0; i < 100; i++ {
			x := nextRandom(&seed)%20001 - 10000
			y := nextRandom(&seed)%20001 - 10000
			ghosts = append(ghosts, [2]int64{x, y})
		}
		boards = append(boards, ghosts)
	}
	rounds := int64(10000000)
	escapes, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		x := nextRandom(&seed)%2001 - 1000
		y := nextRandom(&seed)%2001 - 1000
		if escapeGhosts(boards[r%64], [2]int64{x, y}) {
			escapes++
			check = (check*31 + r%1000) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 100-ghost boards: %d escapes, checksum %d\n", rounds, escapes, check)
}
