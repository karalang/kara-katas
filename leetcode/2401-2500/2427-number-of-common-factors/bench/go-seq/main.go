// LeetCode #2427: Number of Common Factors -- the bench, the ★ arm: the
// divisors of gcd(a, b), counted in pairs up to its square root.
package main

import "fmt"

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func commonFactors(a, b int64) int64 {
	g := gcd(a, b)
	var count int64
	for d := int64(1); d*d <= g; d++ {
		if g%d == 0 {
			if d*d == g {
				count++
			} else {
				count += 2
			}
		}
	}
	return count
}

func main() {
	var check int64
	for p := int64(0); p < 5; p++ {
		for a := int64(1); a <= 1000; a++ {
			for b := int64(1); b <= 1000; b++ {
				other := (b+p-1)%1000 + 1
				check = (check*31 + commonFactors(a, other) + p) % 1000000007
			}
		}
	}
	fmt.Printf("5 passes over 10^6 pairs: checksum %d\n", check)
}
