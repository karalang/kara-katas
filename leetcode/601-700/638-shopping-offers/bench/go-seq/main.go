// Benchmark for #638: mirror of shopping_offers.kara (the ★ arm: search
// over what is still needed, with a memo keyed by the needs) on the same
// workload. Go cannot key a map by a slice, so the needs are a [6]int64
// array, which Go hashes by value.
package main

import "fmt"

const n = 6
const rounds = 800

type need [n]int64

func cheapest(price []int64, special [][]int64, needs need, memo map[need]int64) int64 {
	if known, ok := memo[needs]; ok {
		return known
	}
	var best int64
	for i := 0; i < n; i++ {
		best += needs[i] * price[i]
	}
	for _, offer := range special {
		var rest need
		fits := true
		any := false
		for i := 0; i < n; i++ {
			if offer[i] > needs[i] {
				fits = false
			}
			if offer[i] > 0 {
				any = true
			}
			rest[i] = needs[i] - offer[i]
		}
		if fits && any {
			cost := offer[n] + cheapest(price, special, rest, memo)
			if cost < best {
				best = cost
			}
		}
	}
	memo[needs] = best
	return best
}

func shoppingOffers(price []int64, special [][]int64, needs need) int64 {
	return cheapest(price, special, needs, map[need]int64{})
}

var seed int64 = 638

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var prices [][]int64
	var needs []need
	var offers [][][]int64
	for s := 0; s < 20; s++ {
		price := make([]int64, n)
		var nd need
		for i := 0; i < n; i++ {
			price[i] = 1 + nextRandom()%10
			nd[i] = nextRandom() % 5
		}
		var special [][]int64
		for o := 0; o < 100; o++ {
			offer := make([]int64, n+1)
			for i := 0; i < n; i++ {
				offer[i] = nextRandom() % 3
			}
			offer[n] = nextRandom() % 51
			special = append(special, offer)
		}
		prices = append(prices, price)
		needs = append(needs, nd)
		offers = append(offers, special)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		s := round % 20
		paid := shoppingOffers(prices[s], offers[s], needs[s])
		total += paid
		checksum = (checksum*31 + paid) % 1000000007
	}
	fmt.Printf("20 shops, %d rounds: total %d, checksum %d\n", rounds, total, checksum)
}
