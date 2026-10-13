// Benchmark for #531: Go mirror of the ★ arm (count each row and
// column); see ../find_lonely_pixel.kara.
package main

import "fmt"

func findLonelyPixel(picture [][]rune) int64 {
	m, n := len(picture), len(picture[0])
	rows := make([]int64, m)
	cols := make([]int64, n)
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			if picture[r][c] == 'B' {
				rows[r]++
				cols[c]++
			}
		}
	}
	var lonely int64
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			if picture[r][c] == 'B' && rows[r] == 1 && cols[c] == 1 {
				lonely++
			}
		}
	}
	return lonely
}

func main() {
	// 20 pictures of 500 by 500 made once, black with a chance of 1 to 20
	// in 1,000; then every picture is answered 200 times.
	seed := int64(531)
	var pictures [][][]rune
	for p := 0; p < 20; p++ {
		perMille := int64(1 + p)
		var picture [][]rune
		for i := 0; i < 500; i++ {
			var row []rune
			for j := 0; j < 500; j++ {
				seed = (seed*1103515245 + 12345) % 2147483648
				if seed/65536%1000 < perMille {
					row = append(row, 'B')
				} else {
					row = append(row, 'W')
				}
			}
			picture = append(picture, row)
		}
		pictures = append(pictures, picture)
	}
	var total, checksum int64
	for round := 0; round < 200; round++ {
		for p := range pictures {
			answer := findLonelyPixel(pictures[p])
			total += answer
			checksum = (checksum*31 + answer) % 1000000007
		}
	}
	fmt.Printf("20 pictures of 500 by 500, 200 times each: total %d, checksum %d\n", total, checksum)
}
