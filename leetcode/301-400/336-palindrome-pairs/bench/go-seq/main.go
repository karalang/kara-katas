// Benchmark workload for LeetCode #336 — Go mirror of palindrome_pairs.kara.
package main

import (
	"fmt"
	"sort"
)

const (
	words_  = 20000
	punches = 50
	modulus = 1073741789
)

func isPalindrome(b string, lo, hi int) bool {
	i, j := lo, hi-1
	for i < j {
		if b[i] != b[j] {
			return false
		}
		i++
		j--
	}
	return true
}

func reversed(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}

type pair struct{ i, j int64 }

func palindromePairs(words []string) []pair {
	index := make(map[string]int64)
	for i, w := range words {
		index[reversed(w)] = int64(i)
	}
	var pairs []pair
	for ii, w := range words {
		i := int64(ii)
		n := len(w)
		for k := 0; k <= n; k++ {
			if isPalindrome(w, k, n) {
				if j, ok := index[w[0:k]]; ok && j != i {
					pairs = append(pairs, pair{i, j})
				}
			}
			if k > 0 && isPalindrome(w, 0, k) {
				if j, ok := index[w[k:n]]; ok && j != i {
					pairs = append(pairs, pair{j, i})
				}
			}
		}
	}
	sort.Slice(pairs, func(a, b int) bool {
		if pairs[a].i != pairs[b].i {
			return pairs[a].i < pairs[b].i
		}
		return pairs[a].j < pairs[b].j
	})
	return pairs
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	alphabet := "abc"
	seed := int64(336)
	seen := make(map[string]bool)
	words := make([]string, 0, words_)
	for len(words) < words_ {
		n := 1 + next(&seed)%10
		b := make([]byte, 0, n)
		for k := int64(0); k < n; k++ {
			b = append(b, alphabet[next(&seed)%3])
		}
		w := string(b)
		if !seen[w] {
			seen[w] = true
			words = append(words, w)
		}
	}
	sink := int64(0)
	for p := 0; p < punches; p++ {
		at := next(&seed) % words_
		old := words[at]
		words[at] = old + "d"
		pairs := palindromePairs(words)
		words[at] = old
		sink = (sink*1000003 + int64(len(pairs))) % modulus
		for _, q := range pairs {
			sink = (sink*31 + q.i*7 + q.j) % modulus
		}
	}
	fmt.Println(sink)
}
