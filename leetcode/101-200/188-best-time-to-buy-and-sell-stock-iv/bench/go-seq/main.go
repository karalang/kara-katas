package main

import "fmt"

func maxI64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func maxProfit(k int64, prices []int64) int64 {
	n := int64(len(prices))
	if n == 0 || k == 0 {
		return 0
	}
	if k >= n/2 {
		var profit int64 = 0
		for i := int64(1); i < n; i++ {
			if prices[i] > prices[i-1] {
				profit += prices[i] - prices[i-1]
			}
		}
		return profit
	}

	var neg int64 = -1000000000
	buy := make([]int64, k+1)
	sell := make([]int64, k+1)
	for j := int64(0); j <= k; j++ {
		buy[j] = neg
		sell[j] = 0
	}
	for d := int64(0); d < n; d++ {
		price := prices[d]
		for t := int64(1); t <= k; t++ {
			buy[t] = maxI64(buy[t], sell[t-1]-price)
			sell[t] = maxI64(sell[t], buy[t]+price)
		}
	}
	return sell[k]
}

func main() {
	var n int64 = 2000
	var kmax int64 = 50
	var rounds int64 = 5000

	prices := make([]int64, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		prices[i] = (state >> 16) % 1000
	}

	var sink int64 = 0
	for round := int64(0); round < rounds; round++ {
		state = (state*1103515245 + 12345) & 2147483647
		k := 1 + state%kmax
		state = (state*1103515245 + 12345) & 2147483647
		idx := state % n
		prices[idx] = (state >> 16) % 1000
		sink += maxProfit(k, prices)
	}
	fmt.Println(sink)
}
