// LeetCode #1359 bench -- Go: the product of i (2i - 1) for i from 1 to n,
// modulo 10^9 + 7.
package main

import "fmt"

const mod = 1000000007

func countOrders(n int32) int32 {
	var count int64 = 1
	for i := int64(1); i <= int64(n); i++ {
		count = count * i % mod * (2*i - 1) % mod
	}
	return int32(count)
}

func main() {
	// 3 * 10^5 questions, each n from 1 to 500 drawn from the checksum so
	// far, every answer folded into it
	var check int64
	for r := int64(0); r < 300000; r++ {
		n := int32(1 + check%500)
		check = (check*31 + int64(countOrders(n)) + r) % mod
	}
	fmt.Printf("300000 questions: checksum %d\n", check)
}
