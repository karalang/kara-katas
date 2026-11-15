// LeetCode #2189: Number of Ways to Build House of Cards -- the
// benchmark's Go mirror of cards.kara: a 0/1 knapsack over the row
// widths.
package main

import "fmt"

func houseOfCards(n int64) int64 {
	ways := make([]int64, n+1)
	ways[0] = 1
	for k := int64(1); 3*k-1 <= n; k++ {
		cost := 3*k - 1
		for s := n; s >= cost; s-- {
			ways[s] += ways[s-cost]
		}
	}
	return ways[n]
}

var seed int64 = 2189

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for i := 0; i < 20000; i++ {
		n := nextRandom()%500 + 1
		check = (check*31 + houseOfCards(n)%1000000007) % 1000000007
	}
	fmt.Printf("20000 solves: checksum %d\n", check)
}
