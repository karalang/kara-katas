// LeetCode 788 — Rotated Digits: the bench, in Go.
// Mirrors rotated_digits.kara: every number up to n checked digit by
// digit, for 50,000 random n.
package main

import "fmt"

func rotatedDigits(n int64) int64 {
	good := int64(0)
	for x := int64(1); x <= n; x++ {
		rest := x
		valid, changed := true, false
		for rest > 0 {
			d := rest % 10
			if d == 3 || d == 4 || d == 7 {
				valid = false
				break
			}
			if d == 2 || d == 5 || d == 6 || d == 9 {
				changed = true
			}
			rest /= 10
		}
		if valid && changed {
			good++
		}
	}
	return good
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(788)
	rounds := int64(50000)
	sum, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		n := 1 + nextRandom(&seed)%10000
		good := rotatedDigits(n)
		sum += good
		check = (check*31 + good) % 1000000007
	}
	fmt.Printf("%d rounds of n up to 10000: answers sum to %d, checksum %d\n", rounds, sum, check)
}
