// LeetCode #727: Minimum Window Subsequence -- forward, then back.
// Benchmark mirror of the Kara star arm: walk s1 forward matching s2 in
// order, walk back from where the last letter matched to find the
// latest start, keep the window if shorter, and begin again one place
// after its start.
package main

import (
	"fmt"
	"strings"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(n, kinds int64, seed *int64) string {
	var sb strings.Builder
	for i := int64(0); i < n; i++ {
		sb.WriteByte(byte('a' + nextRandom(seed)%kinds))
	}
	return sb.String()
}

func minWindow(s1, s2 string) string {
	n, m := int64(len(s1)), int64(len(s2))
	bestStart, bestLen := int64(-1), n+1
	i := int64(0)
	for i < n {
		j := int64(0)
		for i < n {
			if s1[i] == s2[j] {
				j++
				if j == m {
					break
				}
			}
			i++
		}
		if j < m {
			break
		}
		end, k, p := i, m-1, i
		for k >= 0 {
			if s1[p] == s2[k] {
				k--
			}
			p--
		}
		start := p + 1
		if end-start+1 < bestLen {
			bestLen = end - start + 1
			bestStart = start
		}
		i = start + 1
	}
	if bestStart < 0 {
		return ""
	}
	return s1[bestStart : bestStart+bestLen]
}

func main() {
	seed := int64(727)
	texts := make([]string, 0, 10)
	for d := 0; d < 10; d++ {
		texts = append(texts, randomWord(20000, 8, &seed))
	}
	sum := 0
	for r := 0; r < 300; r++ {
		for d := 0; d < 10; d++ {
			word := randomWord(20, 8, &seed)
			sum += len(minWindow(texts[d], word))
		}
	}
	fmt.Printf("300 rounds of 10 texts of 20000 letters: sum %d\n", sum)
}
