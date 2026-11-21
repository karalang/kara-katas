// LeetCode #2507: Smallest Value After Replacing With Sum of Prime
// Factors -- Go mirror of the benchmark (smallest.kara): the same passes,
// order and checksum.
package main

import "fmt"

func smallestValue(n int64) int64 {
	for {
		rest, total := n, int64(0)
		for p := int64(2); p*p <= rest; p++ {
			for rest%p == 0 {
				rest /= p
				total += p
			}
		}
		if rest > 1 {
			total += rest
		}
		if total == n {
			return n
		}
		n = total
	}
}

func main() {
	const passes = 14
	var check int64
	for p := int64(0); p < passes; p++ {
		start := check % 99999
		for k := int64(0); k < 99999; k++ {
			n := (start+k)%99999 + 2
			check = (check*31 + smallestValue(n) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 2 to 10^5: checksum %d\n", passes, check)
}
