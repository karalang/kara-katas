// LeetCode #1754: Largest Merge Of Two Strings -- the bench (merge.kara in
// Go): the larger rest goes first.
package main

import (
	"fmt"
	"strings"
)

func largestMerge(word1, word2 string) string {
	var merge strings.Builder
	i, j := 0, 0
	for i < len(word1) || j < len(word2) {
		if word1[i:] > word2[j:] {
			merge.WriteString(word1[i : i+1])
			i++
		} else {
			merge.WriteString(word2[j : j+1])
			j++
		}
	}
	return merge.String()
}

var seed int64 = 1754

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// `n` letters, `a` but for a `b` one time in 300, so that the two rests
// often tie for a long way
func word(n int) string {
	var s strings.Builder
	for i := 0; i < n; i++ {
		if nextRandom()%300 == 0 {
			s.WriteString("b")
		} else {
			s.WriteString("a")
		}
	}
	return s.String()
}

func main() {
	const count, rounds, n = 200, 20, 3000
	pairs := make([][2]string, count)
	for c := range pairs {
		pairs[c][0] = word(n)
		pairs[c][1] = word(n)
	}
	var check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range pairs {
			merge := largestMerge(p[0], p[1])
			check = (check*31 + r) % 1000000007
			for k := 0; k < len(merge); k++ {
				check = (check*31 + int64(merge[k])) % 1000000007
			}
		}
	}
	fmt.Printf("%d pairs of %d letters, %d rounds: checksum %d\n", count, n, rounds, check)
}
