// LeetCode #937: Reorder Data in Log Files -- bench: two lists and a
// sort. Mirrors reorder_log_files.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

type logEntry struct {
	contents string
	id       string
	log      string
}

func reorderLogFiles(logs []string) []string {
	letters := []logEntry{}
	digits := []string{}
	for _, log := range logs {
		cut := strings.IndexByte(log, ' ')
		contents := log[cut+1:]
		first := contents[0]
		if first >= '0' && first <= '9' {
			digits = append(digits, log)
		} else {
			letters = append(letters, logEntry{contents, log[:cut], log})
		}
	}
	sort.SliceStable(letters, func(i, j int) bool {
		if letters[i].contents != letters[j].contents {
			return letters[i].contents < letters[j].contents
		}
		return letters[i].id < letters[j].id
	})
	out := make([]string, 0, len(logs))
	for _, e := range letters {
		out = append(out, e.log)
	}
	return append(out, digits...)
}

var seed int64 = 937

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds = 200
	const count = 200
	lists := [][]string{}
	for c := 0; c < count; c++ {
		logs := []string{}
		for i := 0; i < 100; i++ {
			b := []byte{byte(97 + nextRandom()%26)}
			b = append(b, strconv.Itoa(i)...)
			digits := nextRandom()%2 == 1
			size := int(20 + nextRandom()%81)
			for len(b)+2 <= size {
				w := int(1 + nextRandom()%8)
				if len(b)+1+w > size {
					w = size - len(b) - 1
				}
				b = append(b, ' ')
				for k := 0; k < w; k++ {
					if digits {
						b = append(b, byte(48+nextRandom()%10))
					} else {
						b = append(b, byte(97+nextRandom()%5))
					}
				}
			}
			logs = append(logs, string(b))
		}
		lists = append(lists, logs)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			out := reorderLogFiles(lists[(r+i)%count])
			total += int64(len(out))
			for _, log := range out {
				for k := 0; k < len(log) && log[k] != ' '; k++ {
					check = (check*131 + int64(log[k])) % 1000000007
				}
			}
		}
	}
	fmt.Printf("%d rounds over %d lists of 100 logs: %d logs, checksum %d\n", rounds, count, total, check)
}
