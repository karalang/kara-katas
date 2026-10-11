// Benchmark for #371 -- mirror of sum.kara.
package main

import "fmt"

func getSum(a, b int64) int64 {
	x, carry := a, b
	for carry != 0 {
		both := x & carry
		x ^= carry
		carry = both << 1
	}
	return x
}

func main() {
	var seed int64 = 371
	var checksum int64
	for i := 0; i < 5000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		a := (seed/65536)%2001 - 1000
		seed = (seed*1103515245 + 12345) % 2147483648
		b := (seed/65536)%2001 - 1000
		checksum = (checksum*31 + getSum(a, b) + 5000) % 1000000007
	}
	fmt.Printf("checksum %d\n", checksum)
}
