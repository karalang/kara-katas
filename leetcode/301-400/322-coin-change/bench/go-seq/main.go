// Benchmark mirror of LeetCode #322 — same bottom-up table as
// bench/coin_change.kara.
package main

import "fmt"

const (
	AMOUNT  = 1000000
	COINS   = 20
	TOP     = 3000
	PASSES  = 24
	STRIDE  = 9973
	MODULUS = 1073741789
)

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func draw(seed *int64, bound int64) int64 {
	hi := next(seed)
	lo := next(seed)
	return (hi*32768 + lo) % bound
}

func fewest(coins []int64, amount int64, best []int64) int64 {
	unreachable := amount + 1
	best[0] = 0
	for a := int64(1); a <= amount; a++ {
		b := unreachable
		for _, c := range coins {
			if c <= a && best[a-c]+1 < b {
				b = best[a-c] + 1
			}
		}
		best[a] = b
	}
	if best[amount] == unreachable {
		return -1
	}
	return best[amount]
}

func contains(v []int64, x int64) bool {
	for _, y := range v {
		if y == x {
			return true
		}
	}
	return false
}

func main() {
	var seed int64 = 322
	var sink int64
	var reached int64
	best := make([]int64, AMOUNT+1)

	for p := 0; p < PASSES; p++ {
		g := int64(1 + p%3)
		coins := make([]int64, 0, COINS)
		for len(coins) < COINS {
			c := g * (draw(&seed, TOP/g) + 1)
			if !contains(coins, c) {
				coins = append(coins, c)
			}
		}
		amount := int64(AMOUNT/2) + draw(&seed, AMOUNT/2+1)
		ans := fewest(coins, amount, best)
		if ans >= 0 {
			reached++
		}
		var probe int64
		for a := int64(0); a <= amount; a += STRIDE {
			probe = (probe*31 + best[a]) % MODULUS
		}
		sink = (sink*131 + ans + 1 + probe) % MODULUS
	}

	fmt.Printf("sink %d reached %d\n", sink, reached)
}
