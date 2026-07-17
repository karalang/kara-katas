// Benchmark workload — greedy O(n) Best Time to Buy and Sell Stock II.
// Algorithmic mirror of bench/max_profit.kara. See ../README.md § Benchmarks for N / K and the LCG.
package main

import "fmt"

func maxProfit(prices []int64) int64 {
	var profit int64 = 0
	for i := 1; i < len(prices); i++ {
		d := prices[i] - prices[i-1]
		if d > 0 {
			profit += d
		}
	}
	return profit
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
		sum += maxProfit(data)
	}
	fmt.Println(sum)
}
