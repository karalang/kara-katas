// LeetCode #1111: Maximum Nesting Depth of Two Valid Parentheses Strings
// -- the bench in Go: the ★ arm over the same 16 strings and the same
// valid prefixes, ranging over each string's runes as Kāra's chars() does.
package main

import "fmt"

func maxDepthAfterSplit(seq string) []int32 {
	var depth int32
	answer := make([]int32, 0, len(seq))
	for _, c := range seq {
		if c == '(' {
			answer = append(answer, depth%2)
			depth++
		} else {
			depth--
			answer = append(answer, depth%2)
		}
	}
	return answer
}

var seed int64 = 1111

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomVps(pairs int64) (string, []int) {
	out := []byte{}
	cuts := []int{}
	var opens, depth int64
	for opens < pairs || depth > 0 {
		if opens < pairs && (depth == 0 || nextRandom()%2 == 0) {
			out = append(out, '(')
			opens++
			depth++
		} else {
			out = append(out, ')')
			depth--
			if depth == 0 {
				cuts = append(cuts, len(out))
			}
		}
	}
	return string(out), cuts
}

func main() {
	type entry struct {
		s    string
		cuts []int
	}
	strings := make([]entry, 16)
	for i := range strings {
		s, cuts := randomVps(5000)
		strings[i] = entry{s, cuts}
	}
	var chars, ones, check int64
	for round := 0; round < 1000; round++ {
		for j := range strings {
			e := &strings[j]
			cut := e.cuts[(round*7919+j*104729)%len(e.cuts)]
			answer := maxDepthAfterSplit(e.s[:cut])
			chars += int64(cut)
			for _, g := range answer {
				ones += int64(g)
			}
			check = (check*31 + int64(answer[(round*31+j)%cut])) % 1000000007
		}
	}
	fmt.Printf("1000 rounds over 16 strings of 10000 characters: %d characters, %d in the second group, checksum %d\n", chars, ones, check)
}
