// Benchmark for #651: the best for every count of presses, as the Kara
// ★ arm.
package main

import "fmt"

func maxA(n int64) int64 {
	best := make([]int64, n+1)
	for i := int64(1); i <= n; i++ {
		best[i] = best[i-1] + 1
		for j := int64(1); j < i-2; j++ {
			if v := best[j] * (i - j - 1); v > best[i] {
				best[i] = v
			}
		}
	}
	return best[n]
}

func main() {
	var calls int64 = 200000
	var total, checksum int64
	for c := int64(0); c < calls; c++ {
		a := maxA(1 + (c*37)%150)
		total = (total + a) % 1000000007
		checksum = (checksum*31 + a%1000000007) % 1000000007
	}
	fmt.Printf("%d calls: total %d, checksum %d\n", calls, total, checksum)
}
