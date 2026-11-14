// LeetCode #1156 bench -- mirrors max_rep_opt1.kara: the same 64 texts,
// the same passes, the ★ arm's runs.
package main

import "fmt"

type run struct {
	letter byte
	length int64
}

func maxRepOpt1(text string) int64 {
	b := text
	count := make([]int64, 26)
	for i := 0; i < len(b); i++ {
		count[b[i]-'a']++
	}
	runs := []run{}
	i := 0
	for i < len(b) {
		j := i
		for j < len(b) && b[j] == b[i] {
			j++
		}
		runs = append(runs, run{b[i], int64(j - i)})
		i = j
	}
	var best int64
	for r := 0; r < len(runs); r++ {
		have := count[runs[r].letter-'a']
		best = max(best, min(runs[r].length+1, have))
		if r+2 < len(runs) && runs[r+1].length == 1 && runs[r+2].letter == runs[r].letter {
			best = max(best, min(runs[r].length+runs[r+2].length+1, have))
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	passes := int64(100)
	seed := int64(1156)
	letters := []int64{2, 3, 26}
	texts := make([]string, 0, 64)
	for t := 0; t < 64; t++ {
		b := []byte{}
		for len(b) < 20000 {
			if t%4 == 3 {
				n := 1 + nextRandom(&seed)%40
				for q := int64(0); q < n; q++ {
					b = append(b, 'a')
				}
				b = append(b, byte('b'+nextRandom(&seed)%25))
			} else {
				b = append(b, byte('a'+nextRandom(&seed)%letters[t%4]))
			}
		}
		texts = append(texts, string(b[:20000]))
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, text := range texts {
			check = (check*31 + maxRepOpt1(text) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 64 texts of 20000 letters: checksum %d\n", passes, check)
}
