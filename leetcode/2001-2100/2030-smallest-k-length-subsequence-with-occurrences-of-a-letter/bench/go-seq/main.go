// LeetCode #2030: Smallest K-Length Subsequence With Occurrences of a
// Letter -- the ★ arm in Go, the same algorithm and workload as subseq.kara.
package main

import (
	"fmt"
	"strings"
)

func smallestSubsequence(s string, k int64, want byte, repetition int64) string {
	n := int64(len(s))
	remain := int64(strings.Count(s, string(want)))
	stack := make([]byte, 0)
	var have int64
	for i := int64(0); i < n; i++ {
		c := s[i]
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			if top > c && int64(len(stack))-1+n-i >= k && (top != want || have-1+remain >= repetition) {
				stack = stack[:len(stack)-1]
				if top == want {
					have--
				}
			} else {
				break
			}
		}
		if int64(len(stack)) < k {
			if c == want {
				stack = append(stack, c)
				have++
			} else if k-int64(len(stack)) > repetition-have {
				stack = append(stack, c)
			}
		}
		if c == want {
			remain--
		}
	}
	return string(stack)
}

var seed int64 = 2030

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	texts := make([]string, 10)
	for a := int64(0); a < 10; a++ {
		span := 2 + 3*a
		var b strings.Builder
		var c int64
		for i := 0; i < 50000; i++ {
			r := nextRandom() % 10
			if r < 4 {
				c = (c + 1) % span
			} else if r < 7 {
				c = nextRandom() % span
			}
			b.WriteByte(byte(97 + c))
		}
		texts[a] = b.String()
	}
	var calls, kept, check int64
	for round := int64(0); round < 20; round++ {
		for a := int64(0); a < 10; a++ {
			s := texts[a]
			k := (round*2477+a*911)%50000 + 1
			letter := byte(97 + (round+a)%(2+3*a))
			copies := int64(strings.Count(s, string(letter)))
			m := k
			if copies < m {
				m = copies
			}
			repetition := (round*131+a*17)%m + 1
			got := smallestSubsequence(s, k, letter, repetition)
			calls++
			n := len(got)
			kept += int64(n)
			check = (check*31 + int64(n)) % 1000000007
			check = (check*31 + int64(got[0]) + int64(got[n/2]) + int64(got[n-1])) % 1000000007
		}
	}
	fmt.Printf("%d calls: %d letters kept, checksum %d\n", calls, kept, check)
}
