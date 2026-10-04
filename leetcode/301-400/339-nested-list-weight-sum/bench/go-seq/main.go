// Benchmark mirror of nested_weight_sum.kara (LeetCode #339): parse a list's
// text into the tree, then walk it. Same lists, rounds and sink.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

type Nested struct {
	isList bool
	v      int64
	items  []Nested
}

func depthSum(items []Nested, depth int64) int64 {
	var total int64
	for i := range items {
		if items[i].isList {
			total += depthSum(items[i].items, depth+1)
		} else {
			total += items[i].v * depth
		}
	}
	return total
}

func weightSum(items []Nested) int64 { return depthSum(items, 1) }

func parseList(text []rune, pos *int) []Nested {
	var items []Nested
	*pos++
	for text[*pos] != ']' {
		if text[*pos] == ',' {
			*pos++
		} else if text[*pos] == '[' {
			items = append(items, Nested{isList: true, items: parseList(text, pos)})
		} else {
			var sign int64 = 1
			if text[*pos] == '-' {
				sign = -1
				*pos++
			}
			var v int64
			for text[*pos] >= '0' && text[*pos] <= '9' {
				v = v*10 + int64(text[*pos]-'0')
				*pos++
			}
			items = append(items, Nested{v: sign * v})
		}
	}
	*pos++
	return items
}

func parse(text string) []Nested {
	cs := []rune(text)
	pos := 0
	return parseList(cs, &pos)
}

func next(state *int64) int64 {
	*state = (*state*1103515245 + 12345) % 2147483648
	return *state >> 8
}

func genMember(state *int64, depth, maxDepth int64, out *strings.Builder) {
	if depth < maxDepth && next(state)%3 == 0 {
		out.WriteByte('[')
		count := next(state) % 5
		for k := int64(0); k < count; k++ {
			if k > 0 {
				out.WriteByte(',')
			}
			genMember(state, depth+1, maxDepth, out)
		}
		out.WriteByte(']')
	} else {
		v := next(state)%201 - 100
		out.WriteString(strconv.FormatInt(v, 10))
	}
}

func genText(seed, top, maxDepth int64) string {
	state := seed
	var out strings.Builder
	out.WriteByte('[')
	for k := int64(0); k < top; k++ {
		if k > 0 {
			out.WriteByte(',')
		}
		genMember(&state, 1, maxDepth, &out)
	}
	out.WriteByte(']')
	return out.String()
}

func main() {
	var texts []string
	for s := int64(0); s < 8; s++ {
		texts = append(texts, genText(s*7919+1, 800, 12))
	}
	var hash int64
	for r := 0; r < 4000; r++ {
		items := parse(texts[r%8])
		w := weightSum(items)
		hash = (hash*31 + w + 1000000) % 1000000007
	}
	fmt.Println(hash)
}
