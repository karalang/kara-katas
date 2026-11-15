// LeetCode #1572: Matrix Diagonal Sum -- bench: the ★ arm (two cells a
// row, the centre taken off once) over one matrix of 1001 rows of values
// from 1 to 100, built once; then 200000 rounds, each writing one random
// cell and summing the diagonals again.
package main

import "fmt"

func diagonalSum(mat [][]int64) int64 {
	n := len(mat)
	var total int64
	for i := 0; i < n; i++ {
		total += mat[i][i] + mat[i][n-1-i]
	}
	if n%2 == 1 {
		total -= mat[n/2][n/2]
	}
	return total
}

var seed int64 = 1572

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 1001
	const rounds = 200000
	mat := make([][]int64, n)
	for i := range mat {
		mat[i] = make([]int64, n)
		for j := range mat[i] {
			mat[i][j] = nextRandom()%100 + 1
		}
	}
	var check, total int64
	for k := 0; k < rounds; k++ {
		r := nextRandom() % n
		c := nextRandom() % n
		mat[r][c] = nextRandom()%100 + 1
		sum := diagonalSum(mat)
		total += sum
		check = mix(check, sum)
	}
	fmt.Printf("%d rounds on %d rows: sums total %d, checksum %d\n", rounds, n, total, check)
}
