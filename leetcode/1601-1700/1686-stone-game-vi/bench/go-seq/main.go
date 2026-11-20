// LeetCode #1686: Stone Game VI -- the bench's Go mirror: the ★ arm on 50
// random games of 100000 stones, all drawn first, each answered 10 times.
package main

import (
	"fmt"
	"slices"
)

func stoneGame(alice, bob []int32) int32 {
	n := len(alice)
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	slices.SortFunc(order, func(i, j int) int {
		wi, wj := alice[i]+bob[i], alice[j]+bob[j]
		switch {
		case wi > wj:
			return -1
		case wi < wj:
			return 1
		}
		return 0
	})
	var difference int32
	for turn, i := range order {
		if turn%2 == 0 {
			difference += alice[i]
		} else {
			difference -= bob[i]
		}
	}
	switch {
	case difference > 0:
		return 1
	case difference < 0:
		return -1
	}
	return 0
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1686

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, size, rounds = 50, 100000, 10
	type game struct{ alice, bob []int32 }
	games := make([]game, 0, count)
	for c := 0; c < count; c++ {
		alice := make([]int32, size)
		bob := make([]int32, size)
		for i := 0; i < size; i++ {
			alice[i] = int32(nextRandom()%100 + 1)
			bob[i] = int32(nextRandom()%100 + 1)
		}
		games = append(games, game{alice, bob})
	}
	var wins [3]int64
	var check int64
	for r := int64(0); r < rounds; r++ {
		for _, g := range games {
			answer := stoneGame(g.alice, g.bob)
			wins[answer+1]++
			check = (check*31 + int64(answer) + 2 + r) % 1000000007
		}
	}
	fmt.Printf("%d games of %d stones, %d rounds: Alice %d, Bob %d, draws %d, checksum %d\n", count, size, rounds, wins[2], wins[0], wins[1], check)
}
