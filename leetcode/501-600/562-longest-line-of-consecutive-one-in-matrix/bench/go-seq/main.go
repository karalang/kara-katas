// Benchmark for #562: Go mirror of the ★ arm (one row of running
// counts); see ../longest_line.kara.
package main

import "fmt"

func longestLine(mat [][]int64) int64 {
	n := len(mat[0])
	up := make([]int64, n)
	diag := make([]int64, n)
	anti := make([]int64, n)
	var best int64
	for _, row := range mat {
		nextUp := make([]int64, n)
		nextDiag := make([]int64, n)
		nextAnti := make([]int64, n)
		var across int64
		for j := 0; j < n; j++ {
			if row[j] == 1 {
				across++
				nextUp[j] = up[j] + 1
				if j > 0 {
					nextDiag[j] = diag[j-1] + 1
				} else {
					nextDiag[j] = 1
				}
				if j+1 < n {
					nextAnti[j] = anti[j+1] + 1
				} else {
					nextAnti[j] = 1
				}
				best = max(best, across, nextUp[j], nextDiag[j], nextAnti[j])
			} else {
				across = 0
			}
		}
		up, diag, anti = nextUp, nextDiag, nextAnti
	}
	return best
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 100
	const rounds = 100
	var seed int64 = 562
	matrices := make([][][]int64, 0)
	m := 1
	for g := 0; g < count; g++ {
		percent := 50 + step(&seed)%46
		mat := make([][]int64, 0)
		for i := 0; i < m; i++ {
			row := make([]int64, 0)
			for j := 0; j < 10000/m; j++ {
				if step(&seed)%100 < percent {
					row = append(row, 1)
				} else {
					row = append(row, 0)
				}
			}
			mat = append(mat, row)
		}
		matrices = append(matrices, mat)
		if m == 10000 {
			m = 1
		} else {
			m *= 10
		}
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			got := longestLine(matrices[(round*7+g)%count])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d matrices of 10000 cells, %d rounds: total %d, checksum %d\n", count, rounds, total, checksum)
}
