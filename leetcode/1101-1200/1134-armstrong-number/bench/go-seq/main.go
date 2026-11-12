// LeetCode #1134: Armstrong Number -- the bench in Go, the same algorithm
// and workload as is_armstrong.kara: every number from 1 to 15000000 asked
// in turn.
package main

import "fmt"

func isArmstrong(n int64) bool {
	var k int64
	m := n
	for m > 0 {
		k++
		m /= 10
	}
	var total int64
	m = n
	for m > 0 {
		d := m % 10
		var p int64 = 1
		for i := int64(0); i < k; i++ {
			p *= d
		}
		total += p
		m /= 10
	}
	return total == n
}

func main() {
	var count, sum, check int64
	for n := int64(1); n <= 15000000; n++ {
		if isArmstrong(n) {
			count++
			sum += n
			check = (check*31 + n) % 1000000007
		}
	}
	fmt.Printf("1 to 15000000: %d Armstrong numbers, summing to %d, checksum %d\n", count, sum, check)
}
