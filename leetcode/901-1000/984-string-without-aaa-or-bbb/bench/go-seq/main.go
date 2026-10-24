// Benchmark: LeetCode #984 String Without AAA or BBB -- the ★ arm, greedy,
// reading the tail, on every pair of counts up to LeetCode's 100.
// Mirrors ../str_without_3a3b.kara, .rs, .c and .py.
package main

import (
	"fmt"
	"strings"
)

func strWithout3a3b(a, b int64) string {
	var s strings.Builder
	leftA, leftB := a, b
	for leftA > 0 || leftB > 0 {
		var writeA bool
		if strings.HasSuffix(s.String(), "aa") {
			writeA = false
		} else if strings.HasSuffix(s.String(), "bb") {
			writeA = true
		} else {
			writeA = leftA >= leftB
		}
		if writeA {
			s.WriteByte('a')
			leftA--
		} else {
			s.WriteByte('b')
			leftB--
		}
	}
	return s.String()
}

func main() {
	rounds := int64(100)
	var pairs [][2]int64
	for a := int64(0); a < 101; a++ {
		for b := int64(0); b < 101; b++ {
			if a+b > 0 && a <= 2*b+2 && b <= 2*a+2 {
				pairs = append(pairs, [2]int64{a, b})
			}
		}
	}
	n := int64(len(pairs))
	var letters, check int64
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < n; i++ {
			p := pairs[(r+i)%n]
			s := strWithout3a3b(p[0], p[1])
			length := int64(len(s))
			middle := int64(2)
			if s[length/2] == 'a' {
				middle = 1
			}
			letters += length
			check = (check*31 + length*3 + middle) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d pairs up to 100: %d letters, checksum %d\n", rounds, n, letters, check)
}
