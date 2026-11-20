// LeetCode #1209 bench, in Go: the ★ arm (a stack of runs, each a letter
// and how many times it has come in a row, a run popped when it reaches
// `k`) on 12 strings of 100000 letters drawn once, then 10 rounds over the
// strings with k = 2, 3 and 4, each answer's length and last letter folded
// into a checksum.
package main

import "fmt"

var seed int64 = 1209

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(n int, letters int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%letters)
	}
	return string(b)
}

type run struct {
	c byte
	n int64
}

func removeDuplicates(s string, k int64) string {
	runs := []run{}
	for i := 0; i < len(s); i++ {
		c := s[i]
		if top := len(runs) - 1; top >= 0 && runs[top].c == c {
			runs[top].n++
			if runs[top].n == k {
				runs = runs[:top]
			}
		} else {
			runs = append(runs, run{c, 1})
		}
	}
	out := make([]byte, 0, len(s))
	for _, r := range runs {
		for j := int64(0); j < r.n; j++ {
			out = append(out, r.c)
		}
	}
	return string(out)
}

func main() {
	texts := make([]string, 0, 12)
	for i := 0; i < 12; i++ {
		if i < 4 {
			texts = append(texts, randomText(100000, 2))
		} else if i < 8 {
			texts = append(texts, randomText(100000, 3))
		} else {
			half := []byte(randomText(50000, 26))
			full := make([]byte, 100000)
			copy(full, half)
			for j := range half {
				full[99999-j] = half[j]
			}
			texts = append(texts, string(full))
		}
	}
	var check int64
	for round := int64(0); round < 10; round++ {
		for _, s := range texts {
			for k := int64(2); k < 5; k++ {
				answer := removeDuplicates(s, k)
				var last int64
				if len(answer) > 0 {
					last = int64(answer[len(answer)-1])
				}
				check = (check*131 + int64(len(answer)) + last + round) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds over 12 strings of 100000 letters: checksum %d\n", check)
}
