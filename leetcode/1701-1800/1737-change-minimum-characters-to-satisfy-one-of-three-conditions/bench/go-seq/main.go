// LeetCode #1737: Change Minimum Characters to Satisfy One of Three
// Conditions -- the bench (minimum.kara): letter counts, and every
// boundary tried.
package main

import (
	"fmt"
	"strings"
)

func minCharacters(a, b string) int64 {
	var countA, countB [26]int64
	for _, c := range a {
		countA[c-'a']++
	}
	for _, c := range b {
		countB[c-'a']++
	}
	m, n := int64(len(a)), int64(len(b))
	best := m + n
	for c := 0; c < 26; c++ {
		best = min(best, m+n-countA[c]-countB[c])
	}
	var belowA, belowB int64
	for c := 1; c < 26; c++ {
		belowA += countA[c-1]
		belowB += countB[c-1]
		best = min(best, m-belowA+belowB)
		best = min(best, n-belowB+belowA)
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func word(n int, seed *int64) string {
	var sb strings.Builder
	for i := 0; i < n; i++ {
		sb.WriteRune(rune(97 + nextRandom(seed)%26))
	}
	return sb.String()
}

func main() {
	count := 20
	var rounds int64 = 200
	n := 100000
	var seed int64 = 1737
	as := make([]string, 0, count)
	bs := make([]string, 0, count)
	for p := 0; p < count; p++ {
		as = append(as, word(n, &seed))
		bs = append(bs, word(n, &seed))
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for p := 0; p < count; p++ {
			answer := minCharacters(as[p], bs[p])
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs of %d letters, %d rounds: changes sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
