// Benchmark for #650: the sum of the prime factors, as the Kara ★ arm.
package main

import "fmt"

func minSteps(n int64) int64 {
	rest, steps, p := n, int64(0), int64(2)
	for p*p <= rest {
		for rest%p == 0 {
			steps += p
			rest /= p
		}
		p++
	}
	if rest > 1 {
		steps += rest
	}
	return steps
}

func main() {
	var limit int64 = 1000000
	var total, checksum int64
	for n := int64(1); n <= limit; n++ {
		steps := minSteps(n)
		total += steps
		checksum = (checksum*31 + steps) % 1000000007
	}
	fmt.Printf("1 to %d: total %d, checksum %d\n", limit, total, checksum)
}
