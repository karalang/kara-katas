// Benchmark for #441: mirror of arrange_coins.kara (the closed form with
// an integer square root) on 3,000,000 random n up to 2^31 - 1.
package main

import "fmt"

// The largest r with r * r <= x.
func isqrt(x int64) int64 {
	if x < 2 {
		return x
	}
	r := x
	next := (r + x/r) / 2
	for next < r {
		r = next
		next = (r + x/r) / 2
	}
	return r
}

func arrangeCoins(n int64) int64 {
	return (isqrt(8*n+1) - 1) / 2
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 3000000
	seed := int64(441)
	total := int64(0)
	checksum := int64(0)
	for i := 0; i < count; i++ {
		a := nextRandom(&seed)
		high := a*32768 + nextRandom(&seed)
		n := 1 + (high*2+nextRandom(&seed)%2)%2147483647
		rows := arrangeCoins(n)
		total += rows
		checksum = (checksum*31 + rows) % 1000000007
	}
	fmt.Printf("%d random n: total %d, checksum %d\n", count, total, checksum)
}
