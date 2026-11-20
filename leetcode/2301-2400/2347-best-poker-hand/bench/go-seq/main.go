// LeetCode #2347: Best Poker Hand -- the bench, the ★ arm in Go: a flush
// when every suit equals the first; otherwise the most cards of one rank,
// counted in a table of 14, names the hand.
package main

import (
	"fmt"
	"slices"
)

func bestHand(ranks []int64, suits []byte) string {
	flush := true
	for _, s := range suits {
		if s != suits[0] {
			flush = false
		}
	}
	if flush {
		return "Flush"
	}
	count := make([]int64, 14)
	most := int64(0)
	for _, r := range ranks {
		count[r]++
		if count[r] > most {
			most = count[r]
		}
	}
	if most >= 3 {
		return "Three of a Kind"
	} else if most == 2 {
		return "Pair"
	}
	return "High Card"
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// five different cards of 52, any card already in the hand drawn
	// again
	seed := int64(2347)
	ranks := make([][]int64, 100000)
	suits := make([][]byte, 100000)
	for h := int64(0); h < 100000; h++ {
		cards := make([]int64, 0, 5)
		for len(cards) < 5 {
			card := nextRandom(&seed) % 52
			if !slices.Contains(cards, card) {
				cards = append(cards, card)
			}
		}
		ranks[h] = make([]int64, 5)
		suits[h] = make([]byte, 5)
		for k, card := range cards {
			ranks[h][k] = card%13 + 1
			suits[h][k] = byte(97 + card/13)
		}
	}
	check := int64(0)
	for p := int64(0); p < 30; p++ {
		for h := 0; h < 100000; h++ {
			check = (check*31 + int64(len(bestHand(ranks[h], suits[h]))) + p) % 1000000007
		}
	}
	fmt.Printf("30 passes over 10^5 hands: checksum %d\n", check)
}
