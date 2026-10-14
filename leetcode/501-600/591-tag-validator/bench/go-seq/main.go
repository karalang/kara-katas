// Benchmark for #591: Go mirror of the ★ arm (one scan with a stack of
// open tags); see ../tag_validator.kara. The stack holds the open tags'
// names as strings, which in Go share the code's bytes.
package main

import (
	"fmt"
	"strings"
)

func validName(name string) bool {
	if len(name) < 1 || len(name) > 9 {
		return false
	}
	for _, c := range name {
		if c < 'A' || c > 'Z' {
			return false
		}
	}
	return true
}

func isValid(code string) bool {
	n := len(code)
	stack := []string{}
	i := 0
	for i < n {
		if i > 0 && len(stack) == 0 {
			return false
		}
		if strings.HasPrefix(code[i:], "<![CDATA[") {
			if len(stack) == 0 {
				return false
			}
			k := strings.Index(code[i+9:], "]]>")
			if k < 0 {
				return false
			}
			i += 9 + k + 3
		} else if strings.HasPrefix(code[i:], "</") {
			start := i + 2
			k := strings.IndexByte(code[start:], '>')
			if k < 0 {
				return false
			}
			name := code[start : start+k]
			if len(stack) == 0 || stack[len(stack)-1] != name {
				return false
			}
			stack = stack[:len(stack)-1]
			i = start + k + 1
		} else if code[i] == '<' {
			start := i + 1
			k := strings.IndexByte(code[start:], '>')
			if k < 0 {
				return false
			}
			name := code[start : start+k]
			if !validName(name) {
				return false
			}
			stack = append(stack, name)
			i = start + k + 1
		} else {
			if len(stack) == 0 {
				return false
			}
			i++
		}
	}
	return len(stack) == 0
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func snippet(depth int64, seed *int64) string {
	names := []string{"A", "XY", "ABCDEFGHI", "CODE"}
	texts := []string{"x", " ", ">", "]]>", "!", "[", "y", "/", "...", "<![CDATA[<A>]]>"}
	name := names[step(seed)%int64(len(names))]
	var out strings.Builder
	out.WriteString("<" + name + ">")
	parts := step(seed) % 7
	for p := int64(0); p < parts; p++ {
		if step(seed)%10 < 4 && depth > 0 {
			out.WriteString(snippet(depth-1, seed))
		} else {
			out.WriteString(texts[step(seed)%int64(len(texts))])
		}
	}
	if step(seed)%40 == 0 {
		out.WriteString("</B>")
	} else {
		out.WriteString("</" + name + ">")
	}
	return out.String()
}

func main() {
	count, rounds := 1000, 1000
	seed := int64(591)
	codes := []string{}
	for len(codes) < count {
		code := snippet(4, &seed)
		if len(code) >= 200 && len(code) <= 500 {
			codes = append(codes, code)
		}
	}
	var valid, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			if isValid(codes[(round*7+g)%count]) {
				valid++
				checksum = (checksum*31 + int64(g) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d snippets, %d rounds: %d valid, checksum %d\n", count, rounds, valid, checksum)
}
