// LeetCode #1281 bench, in Go: the ★ arm (the digits by remainders) on
// every n from 1 to 10^5, 2000 rounds, every answer folded into a checksum.
package main

import "fmt"

func subtractProductAndSum(n int64) int64 {
	product, sum, rest := int64(1), int64(0), n
	for rest > 0 {
		digit := rest % 10
		product *= digit
		sum += digit
		rest /= 10
	}
	return product - sum
}

func main() {
	var check int64
	for round := int64(0); round < 2000; round++ {
		for n := int64(1); n <= 100000; n++ {
			check = (check*131 + subtractProductAndSum(n) + round + 1000) % 1000000007
		}
	}
	fmt.Printf("2000 rounds of 1 to 100000: checksum %d\n", check)
}
