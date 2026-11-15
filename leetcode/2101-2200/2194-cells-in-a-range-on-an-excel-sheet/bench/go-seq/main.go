// benchmark's Go mirror of cells.kara (LeetCode #2194, the ★ arm): two
// loops over the range's bytes.
package main

import "fmt"

func cellsInRange(s string) []string {
	cells := []string{}
	for col := s[0]; col <= s[3]; col++ {
		for row := s[1]; row <= s[4]; row++ {
			cells = append(cells, string([]byte{col, row}))
		}
	}
	return cells
}

func main() {
	letters := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	ranges := []string{}
	for c1 := 0; c1 < 26; c1++ {
		for c2 := c1; c2 < 26; c2++ {
			for r1 := 1; r1 < 10; r1++ {
				for r2 := r1; r2 < 10; r2++ {
					ranges = append(ranges, fmt.Sprintf("%c%d:%c%d", letters[c1], r1, letters[c2], r2))
				}
			}
		}
	}
	var check int64
	for p := 0; p < 20; p++ {
		for _, s := range ranges {
			cells := cellsInRange(s)
			last := cells[len(cells)-1]
			check = (check*31 + int64(len(cells))*1000 + int64(last[0])*10 + int64(last[1])) % 1000000007
		}
	}
	fmt.Printf("20 passes over %d ranges: checksum %d\n", len(ranges), check)
}
