// Benchmark for #385: mirror of mini_parser.kara (recursive descent).
package main

import (
	"fmt"
	"strconv"
	"strings"
)

type NestedInteger struct {
	isList bool
	value  int64
	items  []NestedInteger
}

func deserialize(s string) NestedInteger {
	pos := 0
	return parseValue(s, &pos)
}

func parseValue(b string, pos *int) NestedInteger {
	if b[*pos] == '[' {
		*pos++
		x := NestedInteger{isList: true}
		if b[*pos] == ']' {
			*pos++
			return x
		}
		for {
			x.items = append(x.items, parseValue(b, pos))
			if b[*pos] == ',' {
				*pos++
			} else {
				*pos++
				return x
			}
		}
	}
	negative := false
	if b[*pos] == '-' {
		negative = true
		*pos++
	}
	var n int64
	for *pos < len(b) && b[*pos] >= '0' && b[*pos] <= '9' {
		n = n*10 + int64(b[*pos]-'0')
		*pos++
	}
	if negative {
		n = -n
	}
	return NestedInteger{value: n}
}

func shape(x *NestedInteger) (int64, int64, int64) {
	if !x.isList {
		return 0, 1, x.value
	}
	var depth, count, sum int64
	for i := range x.items {
		d, c, s := shape(&x.items[i])
		if d > depth {
			depth = d
		}
		count += c
		sum += s
	}
	return depth + 1, count, sum
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomValue(seed *int64, depth int64, out *strings.Builder) {
	r := next(seed) % 10
	if depth == 0 || r < 4 {
		out.WriteString(strconv.FormatInt(next(seed)%2000001-1000000, 10))
		return
	}
	n := next(seed) % 5
	out.WriteByte('[')
	for i := int64(0); i < n; i++ {
		if i > 0 {
			out.WriteByte(',')
		}
		randomValue(seed, depth-1, out)
	}
	out.WriteByte(']')
}

func main() {
	seed := int64(385)
	var sb strings.Builder
	sb.WriteByte('[')
	for sb.Len() < 49000 {
		if sb.Len() > 1 {
			sb.WriteByte(',')
		}
		randomValue(&seed, 5, &sb)
	}
	sb.WriteByte(']')
	s := sb.String()
	const p = int64(1000000007)
	var checksum int64
	for q := 0; q < 2000; q++ {
		x := deserialize(s)
		depth, count, sum := shape(&x)
		checksum = ((checksum*31+depth*7+count)%p + sum%p + p) % p
	}
	fmt.Printf("%d bytes parsed 2000 times, checksum %d\n", len(s), checksum)
}
