// LeetCode #2806: Account Balance After Rounded Purchase -- the bench in
// Go: the ★ arm over 10^6 amounts from 0 to 100, all drawn first, then
// each answered 100 times into a running checksum.
package main

import "fmt"

func accountBalanceAfterPurchase(purchaseAmount int64) int64 {
	return 100 - (purchaseAmount+5)/10*10
}

var seed int64 = 2806

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 1000000
	rounds := 100
	amounts := make([]int64, count)
	for i := range amounts {
		amounts[i] = nextRandom() % 101
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, p := range amounts {
			b := accountBalanceAfterPurchase(p)
			total += b
			check = (check*31 + b + r) % 1000000007
		}
	}
	fmt.Printf("%d amounts, %d rounds: balances sum to %d, checksum %d\n", count, rounds, total, check)
}
