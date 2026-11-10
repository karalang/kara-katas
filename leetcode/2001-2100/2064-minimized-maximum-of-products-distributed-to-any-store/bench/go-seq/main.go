// LeetCode #2064: Minimized Maximum of Products Distributed to Any Store --
// Go mirror of the ★ arm's benchmark (stores.kara): 200 problems of 50000
// types, quantities from 1 to 100000, and from 50000 to 100000 stores.
package main

import "fmt"

func minimizedMaximum(n int64, quantities []int64) int64 {
	lo, hi := int64(1), int64(0)
	for _, q := range quantities {
		if q > hi {
			hi = q
		}
	}
	for lo < hi {
		mid := (lo + hi) / 2
		need := int64(0)
		for _, q := range quantities {
			need += (q + mid - 1) / mid
		}
		if need <= n {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

var seed int64 = 2064

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	total, check := int64(0), int64(0)
	for t := 0; t < 200; t++ {
		qs := []int64{}
		for i := 0; i < 50000; i++ {
			hi := nextRandom()
			qs = append(qs, (hi*32768+nextRandom())%100000+1)
		}
		hi := nextRandom()
		n := 50000 + (hi*32768+nextRandom())%50001
		a := minimizedMaximum(n, qs)
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("200 problems: sum %d, checksum %d\n", total, check)
}
