// LeetCode #714: Best Time to Buy and Sell Stock with Transaction Fee
// -- two running states. Benchmark mirror of the Kara star arm: the
// best cash holding no share and the best holding one, day by day.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func maxProfit(prices []int64, fee int64) int64 {
	cash, hold := int64(0), -prices[0]
	for i := 1; i < len(prices); i++ {
		sold := hold + prices[i] - fee
		if sold > cash {
			cash = sold
		}
		bought := cash - prices[i]
		if bought > hold {
			hold = bought
		}
	}
	return cash
}

func main() {
	seed := int64(714)
	var walks [][]int64
	for w := int64(1); w <= 10; w++ {
		step := 10 * w
		price := int64(50000)
		prices := make([]int64, 100000)
		for i := range prices {
			price += nextRandom(&seed)%(2*step+1) - step
			if price < 1 {
				price = 1
			}
			prices[i] = price
		}
		walks = append(walks, prices)
	}
	sum := int64(0)
	for round := int64(0); round < 300; round++ {
		fee := 3 * round
		for _, prices := range walks {
			sum += maxProfit(prices, fee)
		}
	}
	fmt.Printf("300 rounds of 10 walks of 100000 days: sum %d\n", sum)
}
