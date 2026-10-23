// LeetCode #901: Online Stock Span -- bench program, Go.
//
// The stack of prices and their spans over 1,000,000 prices built once, a
// random walk between 1 and 10^5 taking steps of -50 to 50. Each round
// gives every price to a fresh spanner, folds the spans into a checksum
// and changes one price.
package main

import "fmt"

type StockSpanner struct {
	prices []int64
	spans  []int64
}

func newStockSpanner() *StockSpanner {
	return &StockSpanner{}
}

func (s *StockSpanner) Next(price int64) int64 {
	var span int64 = 1
	for len(s.prices) > 0 && s.prices[len(s.prices)-1] <= price {
		span += s.spans[len(s.spans)-1]
		s.prices = s.prices[:len(s.prices)-1]
		s.spans = s.spans[:len(s.spans)-1]
	}
	s.prices = append(s.prices, price)
	s.spans = append(s.spans, span)
	return span
}

var seed int64 = 901

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var days int64 = 1000000
	var rounds int64 = 50
	prices := make([]int64, 0, days)
	var p int64 = 50000
	for d := int64(0); d < days; d++ {
		p = p + nextRandom()%101 - 50
		if p < 1 {
			p = 1
		}
		if p > 100000 {
			p = 100000
		}
		prices = append(prices, p)
	}
	var check, total int64
	for round := int64(0); round < rounds; round++ {
		s := newStockSpanner()
		for d := int64(0); d < days; d++ {
			span := s.Next(prices[d])
			total += span
			check = (check*31 + span) % 1000000007
		}
		prices[round*7919%days] = 1 + nextRandom()%100000
	}
	fmt.Printf("%d rounds over %d prices: spans summing to %d, checksum %d\n", rounds, days, total, check)
}
