// Benchmark for #566: Go mirror of the ★ arm (index arithmetic); see
// ../matrix_reshape.kara.
package main

import "fmt"

func matrixReshape(mat [][]int64, r, c int64) [][]int64 {
	m := int64(len(mat))
	n := int64(len(mat[0]))
	if m*n != r*c {
		out := make([][]int64, m)
		for i := range mat {
			out[i] = append([]int64(nil), mat[i]...)
		}
		return out
	}
	out := make([][]int64, 0)
	for i := int64(0); i < r; i++ {
		row := make([]int64, 0)
		for j := int64(0); j < c; j++ {
			k := i*c + j
			row = append(row, mat[k/n][k%n])
		}
		out = append(out, row)
	}
	return out
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := int64(20)
	rounds := int64(800)
	shapes := [10][2]int64{{1, 10000}, {4, 2500}, {25, 400}, {50, 200}, {100, 100}, {200, 50}, {400, 25}, {2500, 4}, {10000, 1}, {99, 101}}
	seed := int64(566)
	mats := make([][][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		mat := make([][]int64, 0, 100)
		for i := 0; i < 100; i++ {
			row := make([]int64, 0, 100)
			for j := 0; j < 100; j++ {
				row = append(row, step(&seed)%2001-1000)
			}
			mat = append(mat, row)
		}
		mats = append(mats, mat)
	}
	var cells, checksum int64
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			shape := shapes[(round+g)%10]
			got := matrixReshape(mats[(round*7+g)%count], shape[0], shape[1])
			rows := int64(len(got))
			cols := int64(len(got[0]))
			cells += rows * cols
			checksum = (checksum*31 + got[round%rows][g%cols] + 1000) % 1000000007
		}
	}
	fmt.Printf("%d matrices of 100 by 100, %d rounds: %d cells, checksum %d\n", count, rounds, cells, checksum)
}
