// LeetCode #885 bench: Go mirror of spiral_matrix_iii.kara (the ★ arm,
// walking the spiral) on the same 6000 grids.
package main

import "fmt"

func spiralMatrixIII(rows, cols, rStart, cStart int64) [][]int64 {
	dr := [4]int64{0, 1, 0, -1}
	dc := [4]int64{1, 0, -1, 0}
	out := [][]int64{{rStart, cStart}}
	r, c := rStart, cStart
	d := 0
	var length int64 = 1
	for int64(len(out)) < rows*cols {
		for leg := 0; leg < 2; leg++ {
			for s := int64(0); s < length; s++ {
				r += dr[d]
				c += dc[d]
				if r >= 0 && r < rows && c >= 0 && c < cols {
					out = append(out, []int64{r, c})
				}
			}
			d = (d + 1) % 4
		}
		length++
	}
	return out
}

var seed int64 = 885

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var cells, check int64
	for g := 0; g < 6000; g++ {
		// 50 x 50 to 100 x 100, the start anywhere
		rows := 50 + nextRandom()%51
		cols := 50 + nextRandom()%51
		rStart := nextRandom() % rows
		cStart := nextRandom() % cols
		out := spiralMatrixIII(rows, cols, rStart, cStart)
		cells += int64(len(out))
		last := len(out) - 1
		check = (check*131 + out[last][0]*101 + out[last][1] + out[len(out)/2][0]) % 1000000007
	}
	fmt.Printf("6000 grids of up to 100 x 100: %d cells, checksum %d\n", cells, check)
}
