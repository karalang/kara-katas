// LeetCode #2396: Strictly Palindromic Number -- the bench, the ★ arm in
// Go: every base tried, each base's digits taken into a list and checked
// from both ends.

package main

import "fmt"

func palindromeInBase(n, b int64) bool {
	var digits []int64
	for m := n; m > 0; m /= b {
		digits = append(digits, m%b)
	}
	for i, j := 0, len(digits)-1; i < j; i, j = i+1, j-1 {
		if digits[i] != digits[j] {
			return false
		}
	}
	return true
}

func isStrictlyPalindromic(n int64) bool {
	for b := int64(2); b < n-1; b++ {
		if !palindromeInBase(n, b) {
			return false
		}
	}
	return true
}

func main() {
	var check, total int64
	for n := int64(4); n <= 10000; n++ {
		var count int64
		for b := int64(2); b < n-1; b++ {
			if palindromeInBase(n, b) {
				count++
			}
		}
		total += count
		s := int64(0)
		if isStrictlyPalindromic(n) {
			s = 1
		}
		check = (check*31 + count + s) % 1000000007
	}
	fmt.Printf("every base of every n from 4 to 10000: checksum %d, %d palindromes\n", check, total)
}
