// Benchmark for #660: base 9, read as base 10, as the Kara ★ arm.
package main

import "fmt"

func newInteger(n int64) int64 {
	rest, place, out := n, int64(1), int64(0)
	for rest > 0 {
		out += rest % 9 * place
		rest /= 9
		place *= 10
	}
	return out
}

func main() {
	count := int64(50000000)
	var checksum int64
	for i := int64(0); i < count; i++ {
		n := 1 + i*16
		checksum = (checksum*31 + newInteger(n)) % 1000000007
	}
	fmt.Printf("%d values of n: checksum %d\n", count, checksum)
}
