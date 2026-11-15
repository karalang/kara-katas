// LeetCode #1163: Last Substring in Lexicographical Order -- Go mirror of the
// Kāra ★ arm: two pointers over the bytes, the answer copied out.
package main

import (
	"fmt"
	"strings"
)

func lastSubstring(s string) string {
	n := len(s)
	i, j, k := 0, 1, 0
	for j+k < n {
		if s[i+k] == s[j+k] {
			k++
		} else if s[i+k] > s[j+k] {
			j = j + k + 1
			k = 0
		} else {
			i = max(i+k+1, j)
			j = i + 1
			k = 0
		}
	}
	return strings.Clone(s[i:])
}

var seed int64 = 1163

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := 400000
	texts := make([]string, 8)
	for k := 0; k < 8; k++ {
		kind := k % 4
		block := make([]byte, 7)
		for i := range block {
			block[i] = byte('a' + nextRandom()%26)
		}
		b := make([]byte, n)
		for i := 0; i < n; i++ {
			switch {
			case kind == 0:
				b[i] = byte('a' + nextRandom()%26)
			case kind == 1:
				b[i] = byte('a' + nextRandom()%2)
			case kind == 2:
				if nextRandom()%1000 == 0 {
					b[i] = byte('a' + nextRandom()%26)
				} else {
					b[i] = block[i%7]
				}
			default:
				if nextRandom()%10 == 0 {
					b[i] = 'y'
				} else {
					b[i] = 'z'
				}
			}
		}
		texts[k] = string(b)
	}
	var total, check int64
	for r := 0; r < 150; r++ {
		for _, t := range texts {
			from := nextRandom() % int64(len(t)/2)
			rest := t[from:]
			got := lastSubstring(rest)
			total += int64(len(got))
			check = (check*31 + int64(len(rest)-len(got))*7 + int64(len(got))) % 1000000007
		}
	}
	fmt.Printf("150 rounds over 8 strings of 4 * 10^5 letters: total %d, checksum %d\n", total, check)
}
