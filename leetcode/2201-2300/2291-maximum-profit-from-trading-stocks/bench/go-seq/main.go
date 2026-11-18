// LeetCode #2291: Maximum Profit From Trading Stocks -- the bench, the ★
// arm in Go. A 0/1 knapsack row over the budget, run downwards for each
// stock that gains.
package main

import "fmt"

func maximumProfit(present, future []int64, budget int64) int64 {
	best := make([]int64, budget+1)
	for i := range present {
		cost := present[i]
		gain := future[i] - present[i]
		if gain <= 0 {
			continue
		}
		for b := budget; b >= cost; b-- {
			if w := best[b-cost] + gain; w > best[b] {
				best[b] = w
			}
		}
	}
	return best[budget]
}

var seed int64 = 2291

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type market struct{ present, future []int64 }
	markets := make([]market, 100)
	for m := range markets {
		present := make([]int64, 500)
		future := make([]int64, 500)
		for i := range present {
			present[i] = nextRandom() % 101
			future[i] = nextRandom() % 101
		}
		markets[m] = market{present, future}
	}
	var check int64
	for _, mk := range markets {
		check = (check*31 + maximumProfit(mk.present, mk.future, 1000)) % 1000000007
	}
	fmt.Printf("100 markets of 500 stocks, budget 1000: checksum %d\n", check)
}
