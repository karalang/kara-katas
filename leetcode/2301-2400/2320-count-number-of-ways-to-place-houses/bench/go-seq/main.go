// LeetCode #2320: Count Number of Ways to Place Houses -- the bench, the
// ★ arm in Go. One side's placements ending in an empty plot and in a
// house rolled forward a plot at a time, and their sum squared. O(n).
package main

import "fmt"

func countHousePlacements(n int64) int64 {
	const modulus = 1000000007
	empty, house := int64(1), int64(1)
	for i := int64(1); i < n; i++ {
		nextEmpty := (empty + house) % modulus
		house = empty
		empty = nextEmpty
	}
	side := (empty + house) % modulus
	return side * side % modulus
}

func main() {
	var check int64
	for p := int64(0); p < 10; p++ {
		for n := int64(1); n <= 10000; n++ {
			check = (check*31 + countHousePlacements(n) + p) % 1000000007
		}
	}
	fmt.Printf("10 passes over every count of plots up to 10^4: checksum %d\n", check)
}
