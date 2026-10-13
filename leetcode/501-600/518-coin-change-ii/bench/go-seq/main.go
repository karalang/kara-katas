// Benchmark for #518: Go mirror of the ★ arm (one row, coins on the
// outside); see ../change.kara.
package main

import "fmt"

func change(amount int64, coins []int64) int64 {
	ways := make([]int64, amount+1)
	ways[0] = 1
	for _, c := range coins {
		for a := c; a <= amount; a++ {
			ways[a] += ways[a-c]
		}
	}
	return ways[amount]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 3,000 random sets of 100 different coins from 500 to 5,000, each
	// with an amount from 4,000 to 5,000 (the problem's most), solved
	// once each. Coins of at least 500 keep every count well inside an
	// int64.
	seed := int64(518)
	sets := 3000
	var checksum int64
	for s := 0; s < sets; s++ {
		amount := 4000 + nextRandom(&seed)%1001
		coins := make([]int64, 0, 100)
		taken := make([]bool, 5001)
		for len(coins) < 100 {
			c := 500 + nextRandom(&seed)%4501
			if !taken[c] {
				taken[c] = true
				coins = append(coins, c)
			}
		}
		checksum = (checksum*31 + change(amount, coins)%1000000007) % 1000000007
	}
	fmt.Printf("%d sets of 100 coins: checksum %d\n", sets, checksum)
}
