// LeetCode #2235: Add Two Integers -- the benchmark's Go mirror of
// add.kara: 10^7 pairs drawn and added, folded into a checksum.
package main

import "fmt"

func sum(num1, num2 int64) int64 {
	return num1 + num2
}

var seed int64 = 2235

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	check := int64(0)
	for i := 0; i < 10000000; i++ {
		num1 := nextRandom()%201 - 100
		num2 := nextRandom()%201 - 100
		check = (check*31 + sum(num1, num2) + 200) % 1000000007
	}
	fmt.Printf("10^7 pairs: checksum %d\n", check)
}
