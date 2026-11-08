// LeetCode #2022: Convert 1D Array Into 2D Array -- the ★ arm in Go, the same
// algorithm and workload as convert.kara.
package main

import "fmt"

func construct2DArray(original []int64, m, n int64) [][]int64 {
	if int64(len(original)) != m*n {
		return [][]int64{}
	}
	grid := make([][]int64, 0, m)
	for i := int64(0); i < m; i++ {
		row := make([]int64, n)
		copy(row, original[i*n:(i+1)*n])
		grid = append(grid, row)
	}
	return grid
}

var seed int64 = 2022

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rowsOf := []int64{1, 2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 125, 200, 250, 400, 500, 1000, 20000}
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		arr := make([]int64, 20000)
		for i := range arr {
			arr[i] = nextRandom()%100000 + 1
		}
		arrays = append(arrays, arr)
	}
	var calls, rows, check int64
	for r := 0; r < 200; r++ {
		for a := 0; a < 20; a++ {
			m := rowsOf[a]
			n := 20000 / m
			if a%5 == 4 {
				n++
			}
			grid := construct2DArray(arrays[a], m, n)
			calls++
			if len(grid) == 0 {
				check = (check*31 + 1000000006) % 1000000007
			}
			for _, row := range grid {
				rows++
				check = (check*31 + row[0] + row[len(row)-1]) % 1000000007
			}
		}
	}
	fmt.Printf("%d calls: %d rows, checksum %d\n", calls, rows, check)
}
