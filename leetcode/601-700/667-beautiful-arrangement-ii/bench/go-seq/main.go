// Benchmark for #667: zigzag from both ends, as the Kara ★ arm.
package main

import "fmt"

func constructArray(n, k int64) []int64 {
	out := []int64{}
	lo, hi := int64(1), k+1
	for lo <= hi {
		out = append(out, lo)
		lo++
		if lo <= hi {
			out = append(out, hi)
			hi--
		}
	}
	for x := k + 2; x <= n; x++ {
		out = append(out, x)
	}
	return out
}

func main() {
	n := int64(10000)
	rounds := int64(10000)
	sum := int64(0)
	for r := int64(0); r < rounds; r++ {
		k := 1 + r*7919%(n-1)
		for _, x := range constructArray(n, k) {
			sum = (sum*31 + x) % 1000000007
		}
	}
	fmt.Printf("n = %d, %d rounds: checksum %d\n", n, rounds, sum)
}
