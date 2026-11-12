// LeetCode #1138: Alphabet Board Path -- the bench, the ★ arm's algorithm:
// coordinates, up and left first, down and right after.
package main

import (
	"fmt"
	"strings"
)

func alphabetBoardPath(target string) string {
	var path strings.Builder
	var row, col int64
	for _, c := range target {
		k := int64(c - 'a')
		r, kCol := k/5, k%5
		path.WriteString(strings.Repeat("U", int(max(row-r, 0))))
		path.WriteString(strings.Repeat("L", int(max(col-kCol, 0))))
		path.WriteString(strings.Repeat("D", int(max(r-row, 0))))
		path.WriteString(strings.Repeat("R", int(max(kCol-col, 0))))
		path.WriteByte('!')
		row, col = r, kCol
	}
	return path.String()
}

var seed int64 = 1138

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := []rune("abcdefghijklmnopqrstuvwxyz")
	targets := make([][]rune, 1000)
	for j := range targets {
		t := make([]rune, 100)
		for i := range t {
			t[i] = letters[nextRandom()%26]
		}
		targets[j] = t
	}
	var total, check int64
	for round := 0; round < 100; round++ {
		for j := 0; j < 1000; j++ {
			targets[j][(round*37+j)%100] = letters[nextRandom()%26]
			target := string(targets[j])
			path := alphabetBoardPath(target)
			mid := int64(path[len(path)/2])
			total += int64(len(path))
			check = (check*31 + int64(len(path))*128 + mid) % 1000000007
		}
	}
	fmt.Printf("100 rounds over 1000 targets of 100 letters: lengths total %d, checksum %d\n", total, check)
}
