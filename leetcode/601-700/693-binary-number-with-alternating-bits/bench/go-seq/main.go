// LeetCode #693: Binary Number with Alternating Bits -- bench program, Go mirror of the ★ arm.
package main

import "fmt"

func hasAlternatingBits(n int64) bool {
	x := n ^ (n >> 1)
	return x&(x+1) == 0
}

func main() {
	var seed int64 = 693
	var count int64 = 100000000
	var yes, checksum int64
	for i := int64(0); i < count; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		n := (int64(1431655765) >> (seed % 31)) ^ ((seed >> 8) % 4)
		if n > 0 && hasAlternatingBits(n) {
			yes++
			checksum = (checksum*31 + n) % 1000000007
		}
	}
	fmt.Printf("%d numbers: %d alternate, checksum %d\n", count, yes, checksum)
}
