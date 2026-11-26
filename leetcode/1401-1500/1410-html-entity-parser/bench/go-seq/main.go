// LeetCode #1410 bench, Go: the same walk, at each `&` the name up to the
// next `;` within seven characters looked up, workload and checksum as
// entity_parser.kara.
package main

import (
	"fmt"
	"strings"
)

func entityParser(text string) string {
	var out strings.Builder
	i := 0
	for i < len(text) {
		if text[i] == '&' {
			w := i + 7
			if w > len(text) {
				w = len(text)
			}
			window := text[i:w]
			if end := strings.IndexByte(window, ';'); end >= 0 {
				symbol := ""
				switch window[:end+1] {
				case "&quot;":
					symbol = "\""
				case "&apos;":
					symbol = "'"
				case "&amp;":
					symbol = "&"
				case "&gt;":
					symbol = ">"
				case "&lt;":
					symbol = "<"
				case "&frasl;":
					symbol = "/"
				}
				if symbol != "" {
					out.WriteString(symbol)
					i += end + 1
					continue
				}
			}
		}
		out.WriteByte(text[i])
		i++
	}
	return out.String()
}

func main() {
	pieces := []string{"a", "b", " ", "&", ";", "&quot;", "&apos;", "&amp;", "&gt;", "&lt;", "&frasl;", "&amp", "&gt",
		"&quot", "&ambassador;", "&lt;;", "&&", "amp;", "&frasl"}
	var seed int64 = 1410
	var pool strings.Builder
	for pool.Len() < 300000 {
		seed = (seed*1103515245 + 12345) % 2147483648
		pool.WriteString(pieces[seed/65536%int64(len(pieces))])
	}
	p := pool.String()
	var check int64
	for r := 0; r < 300; r++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := seed / 65536 % (int64(len(p)) - 100000)
		out := entityParser(p[start : start+100000])
		var sum int64
		for k := 0; k < len(out); k++ {
			sum += int64(out[k])
		}
		check = (check*131 + int64(len(out)) + sum) % 1000000007
	}
	fmt.Printf("300 windows of 10^5 characters: checksum %d\n", check)
}
