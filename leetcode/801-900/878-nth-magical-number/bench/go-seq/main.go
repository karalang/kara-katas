// LeetCode #878 bench: Go mirror of nth_magical_number.kara (the ★ arm,
// binary search on the answer) on the same 1,000,000 cases.
package main

import "fmt"

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func nthMagicalNumber(n, a, b int64) int64 {
	lcm := a / gcd(a, b) * b
	lo, hi := int64(1), n*min(a, b)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if mid/a+mid/b-mid/lcm >= n {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo % 1000000007
}

var seed int64 = 878

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func upTo(limit int64) int64 {
	x := nextRandom()
	y := nextRandom()
	return (x*32768+y)%limit + 1
}

func main() {
	var total, check int64
	for k := 0; k < 1000000; k++ {
		n := upTo(1000000000)
		a := upTo(39999) + 1
		b := upTo(39999) + 1
		answer := nthMagicalNumber(n, a, b)
		total += answer
		check = (check*131 + answer) % 1000000007
	}
	fmt.Printf("1000000 cases: answers sum to %d, checksum %d\n", total, check)
}
