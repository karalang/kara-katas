// LeetCode #2517: Maximum Tastiness of Candy Basket -- Go mirror of the
// benchmark (tastiness.kara): the same lists, passes, order and checksum.
package main

import (
	"fmt"
	"sort"
)

func maximumTastiness(price []int64, k int64) int64 {
	sorted := append([]int64(nil), price...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i] < sorted[j] })
	fits := func(d int64) bool {
		count, last := int64(1), sorted[0]
		for _, p := range sorted {
			if p-last >= d {
				count++
				last = p
			}
		}
		return count >= k
	}
	lo, hi := int64(0), (sorted[len(sorted)-1]-sorted[0])/(k-1)
	for lo < hi {
		mid := lo + (hi-lo+1)/2
		if fits(mid) {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return lo
}

var seed int64 = 2517

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func below(top int64) int64 {
	a := nextRandom()
	b := nextRandom()
	return (a*32768 + b) % top
}

func main() {
	lists := make([][]int64, 20)
	for t := range lists {
		lists[t] = make([]int64, 100000)
		for i := range lists[t] {
			lists[t][i] = below(1000000000) + 1
		}
	}
	const passes = 3
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, price := range lists {
			check = (check*31 + maximumTastiness(price, check%1000+2) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 20 lists of 10^5 prices: checksum %d\n", passes, check)
}
