// LeetCode #734: Sentence Similarity -- a set of pairs.
// Benchmark mirror of the Kara star arm: put every pair in a map used
// as a set, both ways round, then check the words place by place.
package main

import "fmt"

type pair struct{ a, b string }

func areSentencesSimilar(sentence1, sentence2 []string, pairs []pair) bool {
	if len(sentence1) != len(sentence2) {
		return false
	}
	similar := map[pair]struct{}{}
	for _, p := range pairs {
		similar[pair{p.a, p.b}] = struct{}{}
		similar[pair{p.b, p.a}] = struct{}{}
	}
	for i := range sentence1 {
		a, b := sentence1[i], sentence2[i]
		if a != b {
			if _, ok := similar[pair{a, b}]; !ok {
				return false
			}
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(734)
	pairs := make([]pair, 0, 1000)
	for i := 0; i < 1000; i++ {
		a := nextRandom(&seed) % 5000
		b := nextRandom(&seed) % 5000
		pairs = append(pairs, pair{fmt.Sprintf("w%d", a), fmt.Sprintf("w%d", b)})
	}
	s1 := make([]string, 0, 1000)
	s2 := make([]string, 0, 1000)
	for i := 0; i < 1000; i++ {
		p := nextRandom(&seed) % 1000
		if nextRandom(&seed)%2 == 0 {
			s1 = append(s1, pairs[p].a)
			s2 = append(s2, pairs[p].b)
		} else {
			s1 = append(s1, pairs[p].b)
			s2 = append(s2, pairs[p].a)
		}
	}
	similar := 0
	for round := 0; round < 1000; round++ {
		j := nextRandom(&seed) % 1000
		x := nextRandom(&seed) % 5000
		saved := s2[j]
		s2[j] = fmt.Sprintf("w%d", x)
		if areSentencesSimilar(s1, s2, pairs) {
			similar++
		}
		s2[j] = saved
		if areSentencesSimilar(s1, s2, pairs) {
			similar++
		}
	}
	fmt.Printf("1000 rounds of 2 checks of 1000 words with 1000 pairs: %d similar\n", similar)
}
