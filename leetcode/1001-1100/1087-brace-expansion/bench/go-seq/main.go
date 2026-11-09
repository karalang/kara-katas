// Benchmark: LeetCode #1087 Brace Expansion -- mirrors brace_expansion.kara:
// the pattern read into sorted groups and the words built by a depth-first
// walk, over 2000 patterns built once.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func groupsOf(s string) [][]byte {
	groups := [][]byte{}
	var open []byte
	inside := false
	for i := 0; i < len(s); i++ {
		c := s[i]
		switch {
		case c == '{':
			open = []byte{}
			inside = true
		case c == '}':
			sort.Slice(open, func(a, b int) bool { return open[a] < open[b] })
			groups = append(groups, open)
			inside = false
		case c == ',':
		case inside:
			open = append(open, c)
		default:
			groups = append(groups, []byte{c})
		}
	}
	return groups
}

func walk(groups [][]byte, at int, word []byte, out *[]string) []byte {
	if at == len(groups) {
		*out = append(*out, string(word))
		return word
	}
	for _, c := range groups[at] {
		word = append(word, c)
		word = walk(groups, at+1, word, out)
		word = word[:len(word)-1]
	}
	return word
}

func expand(s string) []string {
	groups := groupsOf(s)
	out := []string{}
	walk(groups, 0, []byte{}, &out)
	return out
}

var seed int64 = 1087

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomPattern(most int, k int64) string {
	s := ""
	parts := nextRandom()%8 + 1
	for p := int64(0); p < parts; p++ {
		if nextRandom()%2 == 0 {
			c := string(rune('a' + nextRandom()%k))
			if len(s)+1 <= most {
				s += c
			}
		} else {
			want := int(nextRandom()%k + 1)
			letters := []string{}
			for len(letters) < want {
				c := string(rune('a' + nextRandom()%k))
				seen := false
				for _, l := range letters {
					seen = seen || l == c
				}
				if !seen {
					letters = append(letters, c)
				}
			}
			group := "{" + strings.Join(letters, ",") + "}"
			if len(s)+len(group) <= most {
				s += group
			}
		}
	}
	if s == "" {
		s = "a"
	}
	return s
}

func main() {
	rounds := int64(400)
	patterns := make([]string, 0, 2000)
	for t := int64(0); t < 2000; t++ {
		patterns = append(patterns, randomPattern(50, t%6+1))
	}
	var words, check int64
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 2000; i++ {
			out := expand(patterns[(r*7+i)%2000])
			words += int64(len(out))
			mid := out[len(out)/2]
			check = (check*31 + int64(len(out)) + int64(mid[len(mid)-1])) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 2000 patterns: %d words, checksum %d\n", rounds, words, check)
}
