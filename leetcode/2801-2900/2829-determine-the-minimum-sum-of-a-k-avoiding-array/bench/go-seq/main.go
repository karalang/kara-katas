// LeetCode #2829: Determine the Minimum Sum of a k-avoiding Array -- the
// bench's Go mirror of the ★ arm: the numbers walked up from 1, each
// taken unless its partner k - v was taken before it.
package main

import "fmt"

func minimumSum(n, k int64) int64 {
	taken := make([]bool, n+k+1)
	var count, sum int64
	v := int64(1)
	for count < n {
		if v >= k || !taken[k-v] {
			taken[v] = true
			count++
			sum += v
		}
		v++
	}
	return sum
}

func main() {
	rounds := 2000
	var total, check int64
	for r := 0; r < rounds; r++ {
		for n := int64(1); n <= 50; n++ {
			for k := int64(1); k <= 50; k++ {
				a := minimumSum(n, k)
				total += a
				check = (check*31 + a + int64(r)) % 1000000007
			}
		}
	}
	fmt.Printf("2500 pairs, %d rounds: sums total %d, checksum %d\n", rounds, total, check)
}
