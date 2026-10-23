// LeetCode #921: Minimum Add to Make Parentheses Valid -- bench: one count
// of the open parentheses. Mirrors min_add_to_make_valid.kara.
package main

import "fmt"

func minAddToMakeValid(s string) int64 {
	var open, added int64
	for i := 0; i < len(s); i++ {
		if s[i] == '(' {
			open++
		} else if open > 0 {
			open--
		} else {
			added++
		}
	}
	return added + open
}

var seed int64 = 921

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count, n = 100, 1000, 1000
	// count strings of n parentheses, built once, leaning from ')' to '('
	strings := make([]string, count)
	for i := range strings {
		lean := int64(30 + i%41)
		b := make([]byte, n)
		for j := range b {
			if nextRandom()%100 < lean {
				b[j] = '('
			} else {
				b[j] = ')'
			}
		}
		strings[i] = string(b)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		// each round visits every string, starting from a different one
		for i := 0; i < count; i++ {
			a := minAddToMakeValid(strings[(r+i)%count])
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d strings of %d: answers summing to %d, checksum %d\n", rounds, count, n, total, check)
}
