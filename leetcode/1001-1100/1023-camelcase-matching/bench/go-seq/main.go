// LeetCode #1023: Camelcase Matching -- bench
// Mirrors ../camel_match.kara; see ../../README.md § Benchmarks.
package main

import (
	"fmt"
	"strings"
)

func camelMatch(queries []string, pattern string) []bool {
	p := []rune(pattern)
	answers := []bool{}
	for _, query := range queries {
		i := 0
		ok := true
		for _, c := range query {
			if i < len(p) && c == p[i] {
				i++
			} else if c >= 'A' && c <= 'Z' {
				ok = false
				break
			}
		}
		answers = append(answers, ok && i == len(p))
	}
	return answers
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomLetter(seed *int64, capitals int64) rune {
	upper := nextRandom(seed)%8 < capitals
	k := nextRandom(seed) % 26
	base := int64(97)
	if upper {
		base = 65
	}
	return rune(base + k)
}

type kase struct {
	pattern string
	queries []string
}

func main() {
	const count, rounds = 500, 150
	seed := int64(1023)
	cases := []kase{}
	letters := 0
	for g := 0; g < count; g++ {
		plen := 1 + nextRandom(&seed)%100
		var pb strings.Builder
		for i := int64(0); i < plen; i++ {
			pb.WriteRune(randomLetter(&seed, 2))
		}
		pattern := pb.String()
		p := []rune(pattern)
		queries := []string{}
		for k := 0; k < 100; k++ {
			var q strings.Builder
			if k%2 == 0 {
				left := nextRandom(&seed) % (100 - plen + 1)
				at := 0
				for at < len(p) || left > 0 {
					if left > 0 && (at == len(p) || nextRandom(&seed)%2 == 0) {
						q.WriteRune(randomLetter(&seed, 1))
						left--
					} else {
						q.WriteRune(p[at])
						at++
					}
				}
			} else {
				n := 1 + nextRandom(&seed)%100
				for i := int64(0); i < n; i++ {
					q.WriteRune(randomLetter(&seed, 2))
				}
			}
			letters += q.Len()
			queries = append(queries, q.String())
		}
		cases = append(cases, kase{pattern, queries})
	}
	var matched, check int64
	for r := 0; r < rounds; r++ {
		for _, cs := range cases {
			for k, answer := range camelMatch(cs.queries, cs.pattern) {
				if answer {
					matched++
					check = (check*31 + int64(k) + 1) % 1000000007
				}
			}
		}
	}
	fmt.Printf("%d cases, %d query letters, %d rounds: %d match, checksum %d\n", count, letters, rounds, matched, check)
}
