// LeetCode #1492: The kth Factor of n -- the bench in Go, mirroring
// kth_factor.kara: every i from 1 to n tried in order.
package main

import "fmt"

func kthFactor(n, k int32) int32 {
	left := k
	for i := int32(1); i <= n; i++ {
		if n%i == 0 {
			left--
			if left == 0 {
				return i
			}
		}
	}
	return -1
}

func main() {
	var check int64
	for pass := int64(0); pass < 400; pass++ {
		for n := int64(1); n <= 1000; n++ {
			k := int32(1 + (n+pass+check)%40)
			check = (check*31 + int64(kthFactor(int32(n), k)) + 2) % 1000000007
		}
	}
	fmt.Printf("400 passes over n up to 1000: checksum %d\n", check)
}
