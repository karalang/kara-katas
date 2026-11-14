// LeetCode #1551: Minimum Operations to Make Array Equal -- bench: the ★
// arm (the lower half's distance from the mean, added up place by place)
// for every n from 1 to 10000, in 100 passes. Go mirror of min_operations.kara.
package main

import "fmt"

func minOperations(n int64) int64 {
	operations := int64(0)
	for i := int64(0); i < n/2; i++ {
		operations += n - (2*i + 1)
	}
	return operations
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	check := int64(0)
	for pass := int64(0); pass < 100; pass++ {
		for n := int64(1); n <= 10000; n++ {
			check = mix(check, minOperations(n)+pass)
		}
	}
	fmt.Printf("100 passes over n from 1 to 10000: checksum %d\n", check)
}
