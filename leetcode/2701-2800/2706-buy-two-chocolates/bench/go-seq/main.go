// LeetCode #2706: Buy Two Chocolates -- the bench (chocolates.kara in
// Go): one pass keeping the two cheapest prices.
package main

import "fmt"

func buyChoco(prices []int64, money int64) int64 {
	first, second := int64(101), int64(101)
	for _, p := range prices {
		if p < first {
			second = first
			first = p
		} else if p < second {
			second = p
		}
	}
	cost := first + second
	if cost <= money {
		return money - cost
	}
	return money
}

var seed int64 = 2706

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	prices []int64
	money  int64
}

func main() {
	lists, rounds := 100000, 10
	problems := make([]problem, 0, lists)
	for l := 0; l < lists; l++ {
		prices := make([]int64, 50)
		for i := range prices {
			prices[i] = nextRandom()%100 + 1
		}
		money := nextRandom()%100 + 1
		problems = append(problems, problem{prices, money})
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, p := range problems {
			left := buyChoco(p.prices, p.money)
			sum += left
			check = (check*31 + left + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d lists of 50 prices, %d rounds: money left sums to %d, checksum %d\n", lists, rounds, sum, check)
}
