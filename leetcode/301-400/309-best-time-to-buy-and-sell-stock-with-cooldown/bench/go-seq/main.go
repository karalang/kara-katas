// Benchmark mirror — LeetCode 309, Best Time to Buy and Sell Stock with Cooldown.
// Same three-state DP, same LCG series, same per-pass perturbation and masked
// sink as cooldown.kara. See ../../README.md § Benchmarks.
package main

import "fmt"

func main() {
	const n int64 = 200000
	const passes int64 = 1900

	prices := make([]int64, n)
	state := int64(20309)
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		prices[i] = state%2001 - 1000
	}

	var checksum int64
	for p := int64(0); p < passes; p++ {
		slot := p % n
		prices[slot] = prices[slot] + (checksum & 1)

		hold := -prices[0]
		var sold, rest int64
		for i := int64(1); i < n; i++ {
			prevHold, prevSold, prevRest := hold, sold, rest
			hold = prevHold
			if prevRest-prices[i] > hold {
				hold = prevRest - prices[i]
			}
			sold = prevHold + prices[i]
			rest = prevRest
			if prevSold > rest {
				rest = prevSold
			}
		}
		best := rest
		if sold > best {
			best = sold
		}
		checksum = (checksum + best) & 0x3FFFFFFF
	}
	fmt.Printf("checksum %d\n", checksum)
}
