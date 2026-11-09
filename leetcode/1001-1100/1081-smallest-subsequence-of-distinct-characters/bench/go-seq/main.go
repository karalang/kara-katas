// Benchmark: LeetCode #1081 Smallest Subsequence of Distinct Characters --
// the ★ arm. Mirrors ../smallest_subsequence.kara, .rs, .c and .py.
package main

import "fmt"

func smallestSubsequence(s string) string {
	var last [26]int
	for i := 0; i < len(s); i++ {
		last[s[i]-'a'] = i
	}
	var placed [26]bool
	stack := []byte{}
	for i := 0; i < len(s); i++ {
		b := s[i]
		if placed[b-'a'] {
			continue
		}
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			if top > b && last[top-'a'] > i {
				placed[top-'a'] = false
				stack = stack[:len(stack)-1]
			} else {
				break
			}
		}
		stack = append(stack, b)
		placed[b-'a'] = true
	}
	return string(stack)
}

var seed int64 = 1081

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := int64(100)
	texts := make([]string, 2000)
	for t := int64(0); t < 2000; t++ {
		k := t%26 + 1
		buf := make([]byte, 1000)
		for j := range buf {
			buf[j] = byte('a' + nextRandom()%k)
		}
		texts[t] = string(buf)
	}
	var kept, check int64
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 2000; i++ {
			out := smallestSubsequence(texts[(r*7+i)%2000])
			kept += int64(len(out))
			check = (check*31 + int64(out[len(out)/2]) + i) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 2000 texts of 1000 letters: %d letters kept, checksum %d\n", rounds, kept, check)
}
