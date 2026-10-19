// LeetCode 806 — Number of Lines To Write String: the bench.
//
// 64 strings of 1000 letters, LeetCode's longest, each with widths of
// its own from 2 to 10, are made once; each round counts the lines of
// the next one.
package main

import "fmt"

var seed int64 = 806

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func numberOfLines(widths []int64, s string) (int64, int64) {
	var lines int64 = 1
	var width int64
	for i := 0; i < len(s); i++ {
		w := widths[s[i]-97]
		if width+w > 100 {
			lines++
			width = w
		} else {
			width += w
		}
	}
	return lines, width
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz"
	allWidths := make([][]int64, 0, 64)
	strings := make([]string, 0, 64)
	for i := 0; i < 64; i++ {
		widths := make([]int64, 26)
		for j := range widths {
			widths[j] = 2 + nextRandom()%9
		}
		allWidths = append(allWidths, widths)
		s := make([]byte, 1000)
		for j := range s {
			s[j] = letters[nextRandom()%26]
		}
		strings = append(strings, string(s))
	}
	var rounds int64 = 1000000
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		lines, width := numberOfLines(allWidths[r%64], strings[r%64])
		total += lines
		check = (check*131 + lines*1000 + width) % 1000000007
	}
	fmt.Printf("%d rounds of 1000 letters: %d lines in all, checksum %d\n", rounds, total, check)
}
