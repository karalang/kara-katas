// LeetCode #629: K Inverse Pairs Array -- Go mirror of the Kāra bench.
//
// The ★ arm's rolling DP with a window sum over the same inputs.
package main

import "fmt"

func kInversePairs(n, k int64) int64 {
	const modulus = 1000000007
	row := make([]int64, k+1)
	row[0] = 1
	for i := int64(2); i <= n; i++ {
		next := make([]int64, k+1)
		var window int64
		for j := int64(0); j <= k; j++ {
			window = (window + row[j]) % modulus
			if j >= i {
				window = (window - row[j-i] + modulus) % modulus
			}
			next[j] = window
		}
		row = next
	}
	return row[k]
}

func main() {
	const rounds = 100
	var checksum int64
	for r := int64(0); r < rounds; r++ {
		n := 500 + (r*37)%501
		k := 500 + (r*91)%501
		c := kInversePairs(n, k)
		checksum = (checksum*31 + c) % 1000000007
	}
	fmt.Printf("%d rounds: checksum %d\n", rounds, checksum)
}
