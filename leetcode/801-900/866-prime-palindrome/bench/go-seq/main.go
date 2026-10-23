// LeetCode #866: Prime Palindrome -- Go mirror of the bench program (the
// ★ arm, the odd-length palindromes in order).
package main

import "fmt"

func oddPalindrome(root int64) int64 {
	y := root
	rest := root / 10
	for rest > 0 {
		y = y*10 + rest%10
		rest /= 10
	}
	return y
}

func isPrime(x int64) bool {
	if x < 2 {
		return false
	}
	if x%2 == 0 {
		return x == 2
	}
	for d := int64(3); d*d <= x; d += 2 {
		if x%d == 0 {
			return false
		}
	}
	return true
}

func primePalindrome(n int64) int64 {
	if n >= 8 && n <= 11 {
		return 11
	}
	for root := int64(1); ; root++ {
		y := oddPalindrome(root)
		if y >= n && isPrime(y) {
			return y
		}
	}
}

var seed int64 = 866

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomN() int64 {
	digits := 1 + nextRandom()%8
	low := int64(1)
	for i := int64(1); i < digits; i++ {
		low *= 10
	}
	hi := nextRandom()
	lo := nextRandom()
	return low + (hi*32768+lo)%(9*low)
}

func main() {
	queries := int64(60000)
	var total, check int64
	for q := int64(0); q < queries; q++ {
		n := randomN()
		p := primePalindrome(n)
		total += p
		check = (check*31 + p) % 1000000007
	}
	fmt.Printf("%d random n of 1 to 8 digits: answers sum to %d, checksum %d\n", queries, total, check)
}
