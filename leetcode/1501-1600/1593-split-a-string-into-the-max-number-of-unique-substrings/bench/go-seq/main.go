// LeetCode #1593: Split a String Into the Max Number of Unique Substrings
// -- the bench in Go, mirroring unique_split.kara: backtracking over a map
// of the pieces used.
package main

import "fmt"

func splitFrom(s string, at int, used map[string]bool, best *int) {
	if at == len(s) {
		if len(used) > *best {
			*best = len(used)
		}
		return
	}
	if len(used)+(len(s)-at) <= *best {
		return
	}
	for end := at + 1; end <= len(s); end++ {
		piece := string([]byte(s[at:end]))
		if !used[piece] {
			used[piece] = true
			splitFrom(s, end, used, best)
			delete(used, piece)
		}
	}
}

func maxUniqueSplit(s string) int32 {
	best := 0
	splitFrom(s, 0, map[string]bool{}, &best)
	return int32(best)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1593)
	strings := make([]string, 0)
	for k := 0; k < 20000; k++ {
		b := make([]byte, 16)
		for i := range b {
			b[i] = byte('a' + nextRandom(&seed)%3)
		}
		strings = append(strings, string(b))
	}
	var check, total int64
	for _, s := range strings {
		answer := int64(maxUniqueSplit(s))
		total += answer
		check = (check*31 + answer + 1) % 1000000007
	}
	fmt.Printf("20000 strings of 16 letters: total %d, checksum %d\n", total, check)
}
