// LeetCode #2898: Maximum Linear Stock Score -- the bench's Go mirror
// (stock.kara): a built-in map.
package main

import "fmt"

var seed int64 = 2898

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func maxScore(prices []int64) int64 {
	sums := make(map[int64]int64)
	for i, p := range prices {
		sums[p-int64(i)] += p
	}
	var best int64
	for _, s := range sums {
		if s > best {
			best = s
		}
	}
	return best
}

func main() {
	const count, rounds, n = 20, 20, 100000
	cases := make([][]int64, count)
	for c := 0; c < count; c++ {
		prices := make([]int64, 0, n)
		for i := int64(0); i < n; i++ {
			if c%2 == 0 {
				prices = append(prices, wide()%1000000000+1)
			} else {
				prices = append(prices, 1000000+i-nextRandom()%50)
			}
		}
		cases[c] = prices
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, prices := range cases {
			score := maxScore(prices)
			total += score
			check = (check*31 + score%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: scores total %d, checksum %d\n", count, n, rounds, total, check)
}
