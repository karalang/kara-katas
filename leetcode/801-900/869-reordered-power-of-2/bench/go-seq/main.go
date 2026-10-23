// LeetCode #869: Reordered Power of 2 -- Go mirror of the bench program
// (the ★ arm, digit counts), with the counts in a slice as in the Kāra
// program.
package main

import "fmt"

func digitCounts(x int64) []int64 {
	counts := make([]int64, 10)
	for rest := x; rest > 0; rest /= 10 {
		counts[rest%10]++
	}
	return counts
}

func equal(a, b []int64) bool {
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func reorderedPowerOf2(n int64) bool {
	want := digitCounts(n)
	power := int64(1)
	for k := 0; k < 30; k++ {
		if equal(digitCounts(power), want) {
			return true
		}
		power *= 2
	}
	return false
}

func main() {
	limit := int64(1000000)
	var count, check int64
	for n := int64(1); n <= limit; n++ {
		if reorderedPowerOf2(n) {
			count++
			check = (check*31 + n) % 1000000007
		}
	}
	fmt.Printf("n from 1 to %d: %d true, checksum %d\n", limit, count, check)
}
