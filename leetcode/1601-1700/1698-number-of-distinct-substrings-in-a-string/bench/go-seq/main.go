// LeetCode #1698: Number of Distinct Substrings in a String -- the bench's
// Go mirror: the ★ arm on 100 random strings of 500 letters, each from the
// first 2 to 26 letters of the alphabet, all drawn first, each answered 3
// times.
package main

import "fmt"

func countDistinct(s string) int32 {
	children := [][]int64{make([]int64, 26)}
	var made int32
	for start := 0; start < len(s); start++ {
		node := int64(0)
		for i := start; i < len(s); i++ {
			edge := s[i] - 'a'
			if children[node][edge] == 0 {
				children = append(children, make([]int64, 26))
				children[node][edge] = int64(len(children) - 1)
				made++
			}
			node = children[node][edge]
		}
	}
	return made
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1698

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 100, 3, 500
	const alphabet = "abcdefghijklmnopqrstuvwxyz"
	strings := make([]string, count)
	for c := range strings {
		used := nextRandom()%25 + 2
		b := make([]byte, n)
		for i := range b {
			b[i] = alphabet[nextRandom()%used]
		}
		strings[c] = string(b)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, s := range strings {
			answer := int64(countDistinct(s))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d letters, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, total, check)
}
