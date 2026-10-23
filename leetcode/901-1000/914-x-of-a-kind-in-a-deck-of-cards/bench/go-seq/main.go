// LeetCode #914: X of a Kind in a Deck of Cards -- bench: Go mirror of the
// counts' greatest common divisor in has_groups_size_x.kara.
package main

import "fmt"

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func hasGroupsSizeX(deck []int64) bool {
	largest := int64(0)
	for _, card := range deck {
		if card > largest {
			largest = card
		}
	}
	count := make([]int64, largest+1)
	for _, card := range deck {
		count[card]++
	}
	g := int64(0)
	for _, c := range count {
		g = gcd(g, c)
	}
	return g >= 2
}

var seed int64 = 914

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 20000
	deck := []int64{}
	for v := int64(0); v < 1666; v++ {
		for k := 0; k < 6; k++ {
			deck = append(deck, v*6)
		}
	}
	n := int64(len(deck))
	yes := 0
	check := int64(0)
	for r := 0; r < rounds; r++ {
		high := nextRandom()
		i := (high*32768 + nextRandom()) % n
		old := deck[i]
		deck[i] = old + nextRandom()%3*6
		if deck[i] > 9995 {
			deck[i] = old
		}
		if hasGroupsSizeX(deck) {
			yes++
			check = (check*31 + int64(r)) % 1000000007
		}
		deck[i] = old
	}
	fmt.Printf("%d rounds over %d cards: %d partitioned, checksum %d\n", rounds, n, yes, check)
}
