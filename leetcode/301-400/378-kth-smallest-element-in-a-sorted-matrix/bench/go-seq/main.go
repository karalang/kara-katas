// Benchmark for #378: mirror of kth_smallest.kara.
package main

import "fmt"

func countAtMost(matrix [][]int64, x int64) int64 {
	n := int64(len(matrix))
	count := int64(0)
	row, col := n-1, int64(0)
	for row >= 0 && col < n {
		if matrix[row][col] <= x {
			count += row + 1
			col++
		} else {
			row--
		}
	}
	return count
}

func kthSmallest(matrix [][]int64, k int64) int64 {
	n := len(matrix)
	lo, hi := matrix[0][0], matrix[n-1][n-1]
	for lo < hi {
		mid := lo + (hi-lo)/2
		if countAtMost(matrix, mid) >= k {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	const n = 300
	seed := int64(378)
	checksum := int64(0)
	for rep := 0; rep < 10; rep++ {
		matrix := make([][]int64, 0, n)
		for i := 0; i < n; i++ {
			row := make([]int64, 0, n)
			for j := 0; j < n; j++ {
				seed = (seed*1103515245 + 12345) % 2147483648
				d := (seed / 65536) % 10000
				var v int64
				switch {
				case i == 0 && j == 0:
					v = -1000000000
				case i == 0:
					v = row[j-1] + d
				case j == 0:
					v = matrix[i-1][0] + d
				default:
					v = max(matrix[i-1][j], row[j-1]) + d
				}
				row = append(row, v)
			}
			matrix = append(matrix, row)
		}
		for q := 0; q < 10000; q++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			k := 1 + (seed/65536)%(n*n)
			checksum = (checksum*1009 + kthSmallest(matrix, k) + 1000000000) % 1000000007
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
