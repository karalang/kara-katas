// Benchmark: LeetCode #1096 Brace Expansion II -- Go mirror of
// brace_expansion_ii.kara: the stack arm, two slices of words sorted and
// deduplicated at each `}`, over 64 expressions of up to 60 characters
// built once, each round changing one letter in every expression.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func join(words, part []string) []string {
	out := []string{}
	for _, a := range words {
		for _, b := range part {
			out = append(out, a+b)
		}
	}
	return out
}

func sortDedup(w []string) []string {
	sort.Strings(w)
	out := w[:0]
	for _, s := range w {
		if len(out) == 0 || out[len(out)-1] != s {
			out = append(out, s)
		}
	}
	return out
}

type frame struct{ union, concat []string }

func braceExpansionII(expression string) []string {
	stack := []frame{}
	union := []string{}
	concat := []string{""}
	for _, c := range expression {
		switch c {
		case '{':
			stack = append(stack, frame{union, concat})
			union = []string{}
			concat = []string{""}
		case ',':
			union = append(union, concat...)
			concat = []string{""}
		case '}':
			union = append(union, concat...)
			union = sortDedup(union)
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			concat = join(top.concat, union)
			union = top.union
		default:
			concat = join(concat, []string{string(c)})
		}
	}
	union = append(union, concat...)
	return sortDedup(union)
}

var seed int64 = 1096

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func letter() byte { return byte('a' + nextRandom()%6) }

func option() string {
	var b []byte
	if nextRandom()%4 == 0 {
		b = append(b, '{', letter())
		b = append(b, ',', letter())
		b = append(b, '}', letter())
	} else {
		k := nextRandom()%2 + 1
		for i := int64(0); i < k; i++ {
			b = append(b, letter())
		}
	}
	return string(b)
}

func main() {
	expressions := [][]byte{}
	for len(expressions) < 64 {
		var sb strings.Builder
		for p := 0; p < 5; p++ {
			k := nextRandom()%2 + 2
			options := make([]string, 0, k)
			for i := int64(0); i < k; i++ {
				options = append(options, option())
			}
			sb.WriteString("{" + strings.Join(options, ",") + "}")
		}
		s := sb.String()
		if len(s) <= 60 {
			expressions = append(expressions, []byte(s))
		}
	}
	var total, check int64
	for round := int64(0); round < 200; round++ {
		for j := range expressions {
			e := expressions[j]
			at := (round*7 + int64(j)*13) % int64(len(e))
			if e[at] >= 'a' && e[at] <= 'z' {
				e[at] = byte('a' + (round+int64(j))%6)
			}
			words := braceExpansionII(string(e))
			total += int64(len(words))
			check = (check*31 + int64(len(words))) % 1000000007
			for _, b := range []byte(words[0] + words[len(words)-1]) {
				check = (check*131 + int64(b)) % 1000000007
			}
		}
	}
	fmt.Printf("200 rounds over 64 expressions: %d words, checksum %d\n", total, check)
}
