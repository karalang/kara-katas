// LeetCode #1181: Before and After Puzzle -- the ★ arm in Go: the phrases'
// indices grouped by first word in a map, each phrase's last word looking
// up the phrases that start with it, the puzzles gathered in a map used as
// a set and sorted (Go has no ordered set).
package main

import (
	"fmt"
	"sort"
	"strings"
)

func beforeAndAfterPuzzles(phrases []string) []string {
	starting := map[string][]int{}
	for i, p := range phrases {
		first := p
		if k := strings.IndexByte(p, ' '); k >= 0 {
			first = p[:k]
		}
		starting[first] = append(starting[first], i)
	}
	set := map[string]struct{}{}
	for i, p := range phrases {
		last := p[strings.LastIndexByte(p, ' ')+1:]
		for _, j := range starting[last] {
			if j != i {
				rest := ""
				if k := strings.IndexByte(phrases[j], ' '); k >= 0 {
					rest = phrases[j][k:]
				}
				set[p+rest] = struct{}{}
			}
		}
	}
	puzzles := make([]string, 0, len(set))
	for p := range set {
		puzzles = append(puzzles, p)
	}
	sort.Strings(puzzles)
	return puzzles
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	vocabulary := []string{"a", "be", "cat", "dog", "eel", "fig", "go", "hat"}
	seed := int64(1181)
	problems := [][]string{}
	for t := 0; t < 100; t++ {
		m := 2 + nextRandom(&seed)%7
		phrases := []string{}
		for k := 0; k < 100; k++ {
			n := 1 + nextRandom(&seed)%25
			words := make([]string, n)
			for w := range words {
				words[w] = vocabulary[nextRandom(&seed)%m]
			}
			phrases = append(phrases, strings.Join(words, " "))
		}
		problems = append(problems, phrases)
	}
	rounds := 5
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for _, phrases := range problems {
			puzzles := beforeAndAfterPuzzles(phrases)
			check = (check*131 + int64(len(puzzles))) % 1000000007
			for _, p := range puzzles {
				check = (check*31 + int64(len(p))) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds of 100 problems: checksum %d\n", rounds, check)
}
