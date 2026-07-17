// Benchmark workload — at-most-two-transactions DP, Best Time to Buy and Sell Stock III.
// Algorithmic mirror of bench/max_profit.kara. See ../README.md § Benchmarks for N / K and the LCG.
package main

import "fmt"

func maxProfit(prices []int64) int64 {
	if len(prices) == 0 {
		return 0
	}
	buy1, sell1, buy2, sell2 := -prices[0], int64(0), -prices[0], int64(0)
	for i := 1; i < len(prices); i++ {
		p := prices[i]
		if -p > buy1 {
			buy1 = -p
		}
		if buy1+p > sell1 {
			sell1 = buy1 + p
		}
		if sell1-p > buy2 {
			buy2 = sell1 - p
		}
		if buy2+p > sell2 {
			sell2 = buy2 + p
		}
	}
	return sell2
}

func main() {
	const N = 2000000
	data := make([]int64, N)
	var state int64 = 12345
	for i := 0; i < N; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		data[i] = (state & 4095) + 1
	}
	var sum int64 = 0
	for k := 0; k < 10; k++ {
		r := maxProfit(data)
		sum += r
		data[0] = ((data[0] + r) & 4095) + 1
	}
	fmt.Println(sum)
}
