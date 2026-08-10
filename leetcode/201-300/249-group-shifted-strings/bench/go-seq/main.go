// Benchmark workload for LeetCode #249 — Group Shifted Strings (Go mirror).
// Mirrors group_shifted.kara algorithm-for-algorithm, including the two map
// probes per word (existence check, then insert-or-append).
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func canonical(word string) string {
	b := []byte(word)
	n := len(b)
	if n == 0 {
		return ""
	}
	shift := int64(b[0]) - int64('a')
	var sb strings.Builder
	for i := 0; i < n; i++ {
		c := ((int64(b[i]) - int64('a') - shift) + 26) % 26
		sb.WriteString(strconv.FormatInt(c, 10))
		sb.WriteByte(',')
	}
	return sb.String()
}

func main() {
	var wordsN int64 = 120000
	var rounds int64 = 5

	words := make([]string, 0, wordsN)
	var state int64 = 249249
	for i := int64(0); i < wordsN; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		ln := (state/65536)%10 + 3
		state = (state*1103515245 + 12345) & 2147483647
		seed := (state / 65536) % 40
		state = (state*1103515245 + 12345) & 2147483647
		shift := (state / 65536) % 26

		b := make([]byte, 0, ln)
		for j := int64(0); j < ln; j++ {
			base := (seed*7 + j*11) % 26
			ch := (base + shift) % 26
			b = append(b, byte(97+ch))
		}
		words = append(words, string(b))
	}

	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		table := map[string][]string{}
		var groups int64 = 0
		var keysum int64 = 0
		for _, w := range words {
			key := canonical(w)
			for _, c := range []byte(key) {
				keysum = (keysum*31 + int64(c)) % 1000000007
			}
			if _, ok := table[key]; !ok {
				groups++
			}
			table[key] = append(table[key], w)
		}
		sink = (sink*131 + groups) % 1000000007
		sink = (sink*31 + keysum) % 1000000007
	}
	fmt.Println(sink)
}
