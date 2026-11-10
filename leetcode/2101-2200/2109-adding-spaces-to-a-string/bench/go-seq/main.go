// LeetCode #2109: Adding Spaces to a String -- the benchmark, the same
// algorithm as spaces.kara: one walk over the letters with an index into
// the spaces.
package main

import (
	"fmt"
	"strings"
)

func addSpaces(s string, spaces []int64) string {
	var out strings.Builder
	out.Grow(len(s) + len(spaces))
	next := 0
	for i, c := range s {
		if next < len(spaces) && spaces[next] == int64(i) {
			out.WriteByte(' ')
			next++
		}
		out.WriteRune(c)
	}
	return out.String()
}

var seed int64 = 2109

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type row struct {
	s      string
	spaces []int64
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	rows := make([]row, 0, 20)
	for r := 0; r < 20; r++ {
		var b strings.Builder
		var spaces []int64
		for i := int64(0); i < 300000; i++ {
			b.WriteByte(letters[nextRandom()%52])
			if nextRandom()%3 == 0 {
				spaces = append(spaces, i)
			}
		}
		rows = append(rows, row{b.String(), spaces})
	}
	var total, check int64
	for _, rw := range rows {
		for q := 0; q < 5; q++ {
			got := addSpaces(rw.s, rw.spaces)
			total += int64(len(got))
			for j := 0; j < len(got); j += 997 {
				check = (check*31 + int64(got[j])) % 1000000007
			}
		}
	}
	fmt.Printf("100 strings: %d characters, checksum %d\n", total, check)
}
