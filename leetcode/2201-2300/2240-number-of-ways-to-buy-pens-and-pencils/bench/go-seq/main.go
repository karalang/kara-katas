// LeetCode #2240: Number of Ways to Buy Pens and Pencils -- the
// benchmark's Go mirror of ways.kara: for each number of pens, the
// pencils the rest buys plus none, summed.
package main

import "fmt"

func waysToBuyPensPencils(total, cost1, cost2 int64) int64 {
	ways := int64(0)
	for pens := int64(0); pens*cost1 <= total; pens++ {
		ways += (total-pens*cost1)/cost2 + 1
	}
	return ways
}

var seed int64 = 2240

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	check := int64(0)
	for c := 0; c < 300; c++ {
		// the money at 10^6, a pen from 1 to 10, a pencil up to 10^6
		cost1 := nextRandom()%10 + 1
		cost2 := wideRandom()%1000000 + 1
		check = (check*31 + waysToBuyPensPencils(1000000, cost1, cost2)) % 1000000007
	}
	fmt.Printf("300 cases of 10^6 money: checksum %d\n", check)
}
