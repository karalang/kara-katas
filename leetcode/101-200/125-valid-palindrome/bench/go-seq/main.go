// LeetCode #125 bench harness — Go peer (go build, single-thread).
//
// Same allocating filter-then-compare as the Kāra mirror. Sink = ITERS.
package main

import (
	"fmt"
	"strings"
)

const iters = 3000000

func isAlnum(b byte) bool {
	return (b >= '0' && b <= '9') || (b >= 'a' && b <= 'z') || (b >= 'A' && b <= 'Z')
}

func isPalindrome(s []byte) bool {
	clean := make([]byte, 0, len(s))
	for _, b := range s {
		if isAlnum(b) {
			if b >= 'A' && b <= 'Z' {
				b += 32
			}
			clean = append(clean, b)
		}
	}
	lo, hi := 0, len(clean)-1
	for lo < hi {
		if clean[lo] != clean[hi] {
			return false
		}
		lo++
		hi--
	}
	return true
}

func main() {
	input := []byte(strings.Repeat("A man, a plan, a canal: Panama", 8))
	var sum int64
	for i := 0; i < iters; i++ {
		if isPalindrome(input) {
			sum++
		}
	}
	fmt.Println(sum)
}
