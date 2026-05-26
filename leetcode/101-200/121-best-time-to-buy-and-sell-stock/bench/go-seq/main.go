// LeetCode 121 — one-pass Best Time to Buy and Sell Stock, Go seq mirror.
package main

import "fmt"

func maxProfit(prices []int64) int64 {
	if len(prices) == 0 {
		return 0
	}
	minPrice := prices[0]
	var best int64
	for _, p := range prices[1:] {
		if p < minPrice {
			minPrice = p
		}
		profit := p - minPrice
		if profit > best {
			best = profit
		}
	}
	return best
}

func main() {
	const N = 2_000_000

	data := make([]int64, N)
	state := int64(12345)
	for i := 0; i < N; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		data[i] = (state & 4095) + 1
	}

	var sum int64
	for k := 0; k < 10; k++ {
		sum += maxProfit(data)
	}
	fmt.Println(sum)
}
