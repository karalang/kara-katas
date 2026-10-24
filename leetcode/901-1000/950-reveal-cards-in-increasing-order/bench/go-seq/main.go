// Benchmark: LeetCode #950 Reveal Cards In Increasing Order -- the ★ arm,
// the reveals played on the places, on decks of 1000 cards, LeetCode's
// largest. Mirrors deck_revealed_increasing.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"slices"
)

func deckRevealedIncreasing(deck []int64) []int64 {
	sorted := slices.Clone(deck)
	slices.Sort(sorted)
	n := len(deck)
	places := make([]int, n)
	for i := range places {
		places[i] = i
	}
	out := make([]int64, n)
	for _, card := range sorted {
		place := places[0]
		places = places[1:]
		out[place] = card
		if len(places) > 0 {
			next := places[0]
			places = append(places[1:], next)
		}
	}
	return out
}

var seed int64 = 950

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count, n := 1000, 20, 1000
	decks := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		taken := map[int64]bool{}
		deck := make([]int64, 0, n)
		for len(deck) < n {
			a := nextRandom()
			b := nextRandom()
			v := 1 + (a*32768+b)%1000000
			if !taken[v] {
				taken[v] = true
				deck = append(deck, v)
			}
		}
		decks = append(decks, deck)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			out := deckRevealedIncreasing(decks[(r+i)%count])
			total += out[n-1]
			check = (check*1000003 + out[(r*7+i)%n]) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d decks of %d cards: last cards adding to %d, checksum %d\n", rounds, count, n, total, check)
}
