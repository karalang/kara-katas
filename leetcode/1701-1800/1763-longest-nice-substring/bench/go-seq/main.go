// LeetCode #1763: Longest Nice Substring -- the bench in Go, mirroring
// longest_nice_substring.kara: divide and conquer at each letter whose
// other case is missing, each part copied into a new string as the Kāra
// arm's slices are.
package main

import (
	"fmt"
	"strings"
)

func swap(c byte) byte {
	if c >= 'a' && c <= 'z' {
		return c - 32
	}
	return c + 32
}

func longestNiceSubstring(s string) string {
	for i := 0; i < len(s); i++ {
		if strings.IndexByte(s, swap(s[i])) < 0 {
			left := longestNiceSubstring(strings.Clone(s[:i]))
			right := longestNiceSubstring(strings.Clone(s[i+1:]))
			if len(right) > len(left) {
				return right
			}
			return left
		}
	}
	return strings.Clone(s)
}

func main() {
	seed := int64(1763)
	list := make([]string, 0, 1000)
	for j := 0; j < 1000; j++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		letters := 1 + seed/65536%12
		seed = (seed*1103515245 + 12345) % 2147483648
		upper := seed / 65536 % 101
		var b strings.Builder
		for i := 0; i < 100; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			base := int64(97)
			if seed/65536%100 < upper {
				base = 65
			}
			seed = (seed*1103515245 + 12345) % 2147483648
			b.WriteByte(byte(base + seed/65536%letters))
		}
		list = append(list, b.String())
	}
	check := int64(0)
	for call := int64(0); call < 500000; call++ {
		s := list[(check+call*7919)%1000]
		check = (check*31 + int64(len(longestNiceSubstring(s)))) % 1000000007
	}
	fmt.Printf("500000 calls over 1000 strings: checksum %d\n", check)
}
