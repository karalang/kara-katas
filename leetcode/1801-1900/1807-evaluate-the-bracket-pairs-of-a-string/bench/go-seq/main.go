// LeetCode #1807: Evaluate the Bracket Pairs of a String -- the bench in
// Go: the ★ arm over 40 strings of 10^5 characters and 40 knowledge lists
// of 2 * 10^4 pairs built once, 200 calls.
package main

import (
	"fmt"
	"strings"
)

func evaluate(s string, knowledge [][]string) string {
	values := map[string]string{}
	for _, pair := range knowledge {
		values[strings.Clone(pair[0])] = strings.Clone(pair[1])
	}
	var out strings.Builder
	var key strings.Builder
	inside := false
	for _, c := range s {
		if c == '(' {
			inside = true
		} else if c == ')' {
			if v, ok := values[key.String()]; ok {
				out.WriteString(v)
			} else {
				out.WriteByte('?')
			}
			key = strings.Builder{}
			inside = false
		} else if inside {
			key.WriteRune(c)
		} else {
			out.WriteRune(c)
		}
	}
	return out.String()
}

var seed int64 = 1807

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word(most, letters int64) string {
	n := 1 + nextRandom()%most
	var w strings.Builder
	for i := int64(0); i < n; i++ {
		w.WriteByte(byte(97 + nextRandom()%letters))
	}
	return w.String()
}

func main() {
	texts := make([]string, 0, 40)
	lists := make([][][]string, 0, 40)
	for t := 0; t < 40; t++ {
		var s strings.Builder
		for s.Len() < 99980 {
			if nextRandom()%2 == 0 {
				s.WriteString(word(3, 26))
			} else {
				s.WriteByte('(')
				s.WriteString(word(8, 4))
				s.WriteByte(')')
			}
		}
		texts = append(texts, s.String())
		knowledge := [][]string{}
		seen := map[string]struct{}{}
		for len(knowledge) < 20000 {
			k := word(8, 4)
			if _, ok := seen[k]; !ok {
				seen[k] = struct{}{}
				knowledge = append(knowledge, []string{k, word(10, 26)})
			}
		}
		lists = append(lists, knowledge)
	}
	var check int64
	for call := int64(0); call < 200; call++ {
		s := texts[(check+call)%40]
		knowledge := lists[(check*7+call)%40]
		out := evaluate(s, knowledge)
		check = (check*31 + int64(len(out)) + int64(out[len(out)/2])) % 1000000007
	}
	fmt.Printf("200 calls over 40 strings of 10^5 characters: checksum %d\n", check)
}
