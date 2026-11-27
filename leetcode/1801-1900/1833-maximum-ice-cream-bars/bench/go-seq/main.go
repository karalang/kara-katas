// LeetCode #1833: Maximum Ice Cream Bars -- the bench in Go: the ★ arm over
// 1000 calls on the first 50000 to 99999 of one list of 10^5 bars of 1 to 10^5
// coins, built once, with 10^6 to 10^8 coins, each run's length and coins
// drawn from the checksum so far. Each call copies its run, as the arm takes
// its list by value.
package main

import (
	"fmt"
	"slices"
)

func maxIceCream(costs []int64, coins int64) int64 {
	dearest := slices.Max(costs)
	count := make([]int64, dearest+1)
	for _, c := range costs {
		count[c]++
	}
	left := coins
	var bars int64
	for price := int64(1); price <= dearest; price++ {
		if price > left {
			break
		}
		bought := min(count[price], left/price)
		bars += bought
		left -= bought * price
	}
	return bars
}

var seed int64 = 1833

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	base := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		hi := nextRandom()
		base = append(base, 1+(hi*32768+nextRandom())%100000)
	}
	var check int64
	for call := int64(0); call < 1000; call++ {
		n := 50000 + (check+call)%50000
		coins := 1000000 + (check*7+call)%99000000
		check = (check*31 + maxIceCream(slices.Clone(base[:n]), coins)) % 1000000007
	}
	fmt.Printf("1000 calls: checksum %d\n", check)
}
