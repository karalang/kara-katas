// Benchmark for #672: the cases worked out, as the Kara ★ arm.
package main

import "fmt"

func flipLights(n, m int64) int64 {
	if m == 0 {
		return 1
	}
	if n == 1 {
		return 2
	}
	if n == 2 {
		if m == 1 {
			return 3
		}
		return 4
	}
	if m == 1 {
		return 4
	}
	if m == 2 {
		return 7
	}
	return 8
}

func main() {
	count := int64(100000000)
	sum := int64(0)
	for i := int64(0); i < count; i++ {
		sum = (sum*31 + flipLights(1+i%1000, i/1000%1001)) % 1000000007
	}
	fmt.Printf("%d queries: checksum %d\n", count, sum)
}
