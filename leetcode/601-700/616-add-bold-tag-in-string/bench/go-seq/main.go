// Benchmark mirror for #616: the same workload and algorithm as
// add_bold_tag.kara (mark, then write).
package main

import (
	"fmt"
	"slices"
	"strings"
)

func addBoldTag(s string, words []string) string {
	n := len(s)
	bold := make([]bool, n)
	for i := 0; i < n; i++ {
		for _, word := range words {
			if strings.HasPrefix(s[i:n], word) {
				for k := i; k < i+len(word); k++ {
					bold[k] = true
				}
			}
		}
	}
	var out strings.Builder
	for i := 0; i < n; i++ {
		if bold[i] && (i == 0 || !bold[i-1]) {
			out.WriteString("<b>")
		}
		out.WriteString(s[i : i+1])
		if bold[i] && (i == n-1 || !bold[i+1]) {
			out.WriteString("</b>")
		}
	}
	return out.String()
}

var seed int64 = 616

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(size int64) string {
	b := make([]byte, size)
	for k := range b {
		b[k] = byte(97 + step()%4)
	}
	return string(b)
}

func main() {
	cases, rounds := int64(20), int64(1000)
	var texts []string
	var lists [][]string
	for c := int64(0); c < cases; c++ {
		s := randomText(1000)
		var words []string
		for len(words) < 100 {
			length := 5 + step()%10
			var w string
			if len(words)%2 == 0 {
				at := step() % (1000 - length)
				w = s[at : at+length]
			} else {
				w = randomText(length)
			}
			if !slices.Contains(words, w) {
				words = append(words, w)
			}
		}
		texts = append(texts, s)
		lists = append(lists, words)
	}
	var total, checksum int64
	for r := int64(0); r < rounds; r++ {
		c := (r * 7) % cases
		out := addBoldTag(texts[c], lists[c])
		total += int64(len(out))
		for _, ch := range out {
			checksum = (checksum*31 + int64(ch)) % 1000000007
		}
	}
	fmt.Printf("%d cases, %d rounds: %d characters, checksum %d\n", cases, rounds, total, checksum)
}
