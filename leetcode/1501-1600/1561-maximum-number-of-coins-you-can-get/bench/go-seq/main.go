// LeetCode #1561: Maximum Number of Coins You Can Get -- bench: the ★ arm
// (sorted, every other pile past the n smallest) over 20 lists of 99999
// piles of 1 to 10000 coins, built once, each asked 10 times.
// Go mirror of coins.kara; the copy is sorted by slices.Sort.
package main

import (
	"fmt"
	"slices"
)

func maxCoins(piles []int64) int64 {
	sorted := slices.Clone(piles)
	slices.Sort(sorted)
	n := len(sorted) / 3
	var sum int64
	for i := n; i < len(sorted); i += 2 {
		sum += sorted[i]
	}
	return sum
}

var seed int64 = 1561

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	lists := make([][]int64, 20)
	for l := range lists {
		lists[l] = make([]int64, 99999)
		for i := range lists[l] {
			lists[l][i] = nextRandom()%10000 + 1
		}
	}
	var check, total int64
	for pass := 0; pass < 10; pass++ {
		for _, piles := range lists {
			coins := maxCoins(piles)
			total += coins
			check = mix(check, coins)
		}
	}
	fmt.Printf("10 passes over 20 lists of 99999 piles: %d coins, checksum %d\n", total, check)
}
