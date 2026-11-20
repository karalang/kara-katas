// LeetCode #1258 bench, in Go: the ★ arm (union-find over the pairs'
// words, the groups sorted, every sentence built by a recursive search, the
// sentences sorted) on 100 random cases built once, each 10 pairs of 8
// words and a text of 10 words, 4 of them from the pairs, asked 80 rounds;
// the sentences counted and the middle one of each answer folded into a
// checksum.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func find(parent map[string]string, word string) string {
	up := parent[word]
	if up == word {
		return up
	}
	root := find(parent, up)
	parent[word] = root
	return root
}

func build(choices [][]string, at int, current *[]string, out *[]string) {
	if at == len(choices) {
		*out = append(*out, strings.Join(*current, " "))
		return
	}
	for _, word := range choices[at] {
		*current = append(*current, word)
		build(choices, at+1, current, out)
		*current = (*current)[:len(*current)-1]
	}
}

func generateSentences(synonyms [][]string, text string) []string {
	parent := map[string]string{}
	for _, pair := range synonyms {
		for _, word := range pair {
			if _, ok := parent[word]; !ok {
				parent[word] = word
			}
		}
	}
	for _, pair := range synonyms {
		a := find(parent, pair[0])
		b := find(parent, pair[1])
		if a != b {
			parent[a] = b
		}
	}
	words := make([]string, 0, len(parent))
	for w := range parent {
		words = append(words, w)
	}
	groups := map[string][]string{}
	for _, word := range words {
		root := find(parent, word)
		groups[root] = append(groups[root], word)
	}
	var choices [][]string
	for _, word := range strings.Split(text, " ") {
		if _, ok := parent[word]; ok {
			g := groups[find(parent, word)]
			group := append([]string(nil), g...)
			sort.Strings(group)
			choices = append(choices, group)
		} else {
			choices = append(choices, []string{word})
		}
	}
	var out []string
	var current []string
	build(choices, 0, &current, &out)
	sort.Strings(out)
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(first byte, seed *int64) string {
	var b []byte
	n := nextRandom(seed)%3 + 1
	for i := int64(0); i < n; i++ {
		b = append(b, first+byte(nextRandom(seed)%6))
	}
	return string(b)
}

func randomWords(count int, first byte, seed *int64) []string {
	var words []string
	for len(words) < count {
		w := randomWord(first, seed)
		found := false
		for _, x := range words {
			if x == w {
				found = true
			}
		}
		if !found {
			words = append(words, w)
		}
	}
	return words
}

type benchCase struct {
	synonyms [][]string
	text     string
}

func makeCase(seed *int64) benchCase {
	pool := randomWords(8, 'a', seed)
	plain := randomWords(12, 'p', seed)
	var synonyms [][]string
	for k := 0; k < 10; k++ {
		i := nextRandom(seed) % 8
		j := (i + 1 + nextRandom(seed)%7) % 8
		synonyms = append(synonyms, []string{pool[i], pool[j]})
	}
	var words []string
	for k := 0; k < 10; k++ {
		words = append(words, plain[nextRandom(seed)%12])
	}
	for k := 0; k < 4; k++ {
		words[k*3] = pool[nextRandom(seed)%8]
	}
	return benchCase{synonyms, strings.Join(words, " ")}
}

func main() {
	seed := int64(1258)
	var cases []benchCase
	for i := 0; i < 100; i++ {
		cases = append(cases, makeCase(&seed))
	}
	total := 0
	check := int64(0)
	for r := 0; r < 80; r++ {
		for _, c := range cases {
			sentences := generateSentences(c.synonyms, c.text)
			total += len(sentences)
			for _, b := range []byte(sentences[len(sentences)/2]) {
				check = (check*131 + int64(b)) % 1000000007
			}
		}
	}
	fmt.Printf("80 rounds of 100 cases: %d sentences, checksum %d\n", total, check)
}
