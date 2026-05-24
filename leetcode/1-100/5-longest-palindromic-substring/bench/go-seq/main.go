// LeetCode 5 — expand-around-center, Go seq mirror.
package main

import (
	"fmt"
	"strings"
)

func expand(chars []rune, lo0, hi0 int64) (int64, int64) {
	lo, hi := lo0, hi0
	n := int64(len(chars))
	for lo >= 0 && hi < n && chars[lo] == chars[hi] {
		lo--
		hi++
	}
	return lo + 1, hi - lo - 1
}

func longestPalindrome(s string) (int64, int64) {
	chars := []rune(s)
	n := int64(len(chars))
	var bestStart, bestLen int64
	for i := int64(0); i < n; i++ {
		start, length := expand(chars, i, i)
		if length > bestLen {
			bestStart, bestLen = start, length
		}
		start, length = expand(chars, i, i+1)
		if length > bestLen {
			bestStart, bestLen = start, length
		}
	}
	return bestStart, bestLen
}

func main() {
	data := strings.Repeat("a", 5000)
	var sum int64
	for k := 0; k < 10; k++ {
		start, length := longestPalindrome(data)
		sum += start + length
	}
	fmt.Println(sum)
}
