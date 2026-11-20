// LeetCode #1217 bench, in Go: the ★ arm (the odd and the even chips
// counted, the lesser count the cost) on 20000 sets of 100 chips at
// positions up to 10^9, drawn once; then 20 rounds over the sets, every
// answer folded into a checksum.
package main

import "fmt"

var seed int64 = 1217

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func minCostToMoveChips(position []int64) int64 {
	var odd, even int64
	for _, p := range position {
		if p%2 == 1 {
			odd++
		} else {
			even++
		}
	}
	if odd < even {
		return odd
	}
	return even
}

func main() {
	sets := make([][]int64, 20000)
	for s := range sets {
		chips := make([]int64, 100)
		for i := range chips {
			hi := nextRandom()
			lo := nextRandom()
			chips[i] = (hi*32768+lo)%1000000000 + 1
		}
		sets[s] = chips
	}
	var check int64
	for round := int64(0); round < 20; round++ {
		for _, chips := range sets {
			check = (check*131 + minCostToMoveChips(chips) + round) % 1000000007
		}
	}
	fmt.Printf("20 rounds over 20000 sets of 100 chips: checksum %d\n", check)
}
