// Benchmark for #533: Go mirror of the ★ arm (count each kind of row);
// see ../find_black_pixel.kara.
package main

import (
	"fmt"
	"strings"
)

func findBlackPixel(picture [][]rune, target int64) int64 {
	n := len(picture[0])
	cols := make([]int64, n)
	rows := map[string]int64{}
	for _, row := range picture {
		var key strings.Builder
		var blacks int64
		for c := 0; c < n; c++ {
			key.WriteRune(row[c])
			if row[c] == 'B' {
				cols[c]++
				blacks++
			}
		}
		if blacks == target {
			rows[key.String()]++
		}
	}
	var lonely int64
	for key, count := range rows {
		if count != target {
			continue
		}
		c := 0
		for _, ch := range key {
			if ch == 'B' && cols[c] == target {
				lonely += target
			}
			c++
		}
	}
	return lonely
}

var seed int64 = 533

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomPicture(n, target, planted, extra, percent int64) [][]rune {
	var picture [][]rune
	for k := int64(0); k < planted; k++ {
		cols := make([]int64, n)
		row := make([]rune, n)
		for c := range cols {
			cols[c] = int64(c)
			row[c] = 'W'
		}
		for i := int64(0); i < target; i++ {
			j := i + nextRandom()%(n-i)
			cols[i], cols[j] = cols[j], cols[i]
			row[cols[i]] = 'B'
		}
		copies := target
		if nextRandom()%4 == 0 {
			copies = target + 1
		}
		for c := int64(0); c < copies; c++ {
			picture = append(picture, append([]rune(nil), row...))
		}
	}
	for k := int64(0); k < extra; k++ {
		row := make([]rune, n)
		for c := range row {
			if nextRandom()%100 < percent {
				row[c] = 'B'
			} else {
				row[c] = 'W'
			}
		}
		picture = append(picture, row)
	}
	for i := int64(len(picture)) - 1; i > 0; i-- {
		j := nextRandom() % (i + 1)
		picture[i], picture[j] = picture[j], picture[i]
	}
	return picture
}

func main() {
	// 20 pictures 200 wide made once, the p-th with 20 rows planted for a
	// target of 1 + p % 8 and 80 more black with a chance of 1%; then
	// each picture is answered for every target from 1 to 8, in 100
	// rounds.
	var pictures [][][]rune
	for p := int64(0); p < 20; p++ {
		pictures = append(pictures, randomPicture(200, 1+p%8, 20, 80, 1))
	}
	var total, checksum int64
	for round := 0; round < 100; round++ {
		for p := range pictures {
			for target := int64(1); target <= 8; target++ {
				answer := findBlackPixel(pictures[p], target)
				total += answer
				checksum = (checksum*31 + answer) % 1000000007
			}
		}
	}
	fmt.Printf("20 pictures 200 wide, targets 1 to 8, 100 rounds: total %d, checksum %d\n", total, checksum)
}
