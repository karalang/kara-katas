// Benchmark for #668: binary search on the value, counting by rows, as
// the Kara ★ arm.
package main

import "fmt"

func findKthNumber(m, n, k int64) int64 {
	lo, hi := int64(1), m*n
	for lo < hi {
		mid := lo + (hi-lo)/2
		count := int64(0)
		for i := int64(1); i <= m; i++ {
			c := mid / i
			if c > n {
				c = n
			}
			count += c
		}
		if count >= k {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	rounds := int64(200)
	sum := int64(0)
	for r := int64(0); r < rounds; r++ {
		m := 30000 - r*97%10000
		n := 30000 - r*89%10000
		k := 1 + r*7919813%(m*n)
		sum = (sum*31 + findKthNumber(m, n, k)) % 1000000007
	}
	fmt.Printf("%d rounds: checksum %d\n", rounds, sum)
}
