// Benchmark for #509: Go mirror of the ★ arm (two running values); see
// ../fib.kara.
package main

import "fmt"

func fib(n int64) int64 {
	var a, b int64 = 0, 1
	for i := int64(0); i < n; i++ {
		next := a + b
		a = b
		b = next
	}
	return a
}

func main() {
	// F(n) for n = 0, 1, ..., 30 over and over, 150,000,000 calls, the
	// results added up modulo 10^9 + 7.
	calls := int64(150000000)
	var total int64
	for i := int64(0); i < calls; i++ {
		total = (total + fib(i%31)) % 1000000007
	}
	fmt.Printf("%d calls: total %d\n", calls, total)
}
