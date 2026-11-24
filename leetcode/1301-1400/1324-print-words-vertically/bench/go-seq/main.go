// LeetCode #1324 bench, Go mirror of the Kāra bench: the ★ arm (the words
// split apart, row i made of each word's i-th letter or a space, the row's
// end trimmed) on 100 sentences of 200 letters and spaces built once; then
// 1000 passes, each setting one letter of every sentence from the checksum
// so far, answering it and folding the rows' letters plus the pass into the
// checksum.
package main

import (
	"fmt"
	"strings"
)

func printVertically(s string) []string {
	words := strings.Split(s, " ")
	tallest := 0
	for _, w := range words {
		if len(w) > tallest {
			tallest = len(w)
		}
	}
	rows := []string{}
	for i := 0; i < tallest; i++ {
		var row strings.Builder
		for _, w := range words {
			if i < len(w) {
				row.WriteByte(w[i])
			} else {
				row.WriteByte(' ')
			}
		}
		rows = append(rows, strings.TrimRight(row.String(), " "))
	}
	return rows
}

var seed int64 = 1324

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 200
	sentences := make([][]byte, 0, 100)
	for t := 0; t < 100; t++ {
		var longest int64
		switch t % 4 {
		case 0:
			longest = 3
		case 1:
			longest = 10
		case 2:
			longest = 40
		default:
			longest = 200
		}
		b := []byte{}
		for len(b) < n {
			ln := 1 + nextRandom()%longest
			for k := int64(0); k < ln; k++ {
				if len(b) < n {
					b = append(b, byte('A'+nextRandom()%26))
				}
			}
			if len(b) < n-1 {
				b = append(b, ' ')
			}
		}
		sentences = append(sentences, b)
	}
	var check int64
	for pass := int64(0); pass < 1000; pass++ {
		for t := 0; t < 100; t++ {
			b := sentences[t]
			at := check % n
			if b[at] != ' ' {
				b[at] = byte('A' + check/7%26)
			}
			rows := printVertically(string(b))
			for _, row := range rows {
				for k := 0; k < len(row); k++ {
					check = (check*131 + int64(row[k])) % 1000000007
				}
			}
			check = (check*31 + int64(len(rows)) + pass) % 1000000007
		}
	}
	fmt.Printf("1000 passes over 100 sentences of 200: checksum %d\n", check)
}
