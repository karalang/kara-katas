// LeetCode #1545: Find Kth Bit in Nth Binary String -- bench: the ★ arm (the
// definition's recursion) asked for every place of S_20, two passes. Go
// mirror of kth_bit.kara.
package main

import "fmt"

func findKthBit(n, k int64) byte {
	if n == 1 {
		return '0'
	}
	middle := int64(1) << (n - 1)
	if k == middle {
		return '1'
	} else if k < middle {
		return findKthBit(n-1, k)
	} else if findKthBit(n-1, (int64(1)<<n)-k) == '0' {
		return '1'
	}
	return '0'
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	check, ones := int64(0), int64(0)
	for p := 0; p < 2; p++ {
		for k := int64(1); k < 1048576; k++ {
			bit := int64(0)
			if findKthBit(20, k) == '1' {
				bit = 1
			}
			ones += bit
			check = mix(check, bit)
		}
	}
	fmt.Printf("2 passes over every place of S_20: %d ones, checksum %d\n", ones, check)
}
