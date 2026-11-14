// LeetCode #2133: Check if Every Row and Column Contains All Numbers --
// the benchmark, the same algorithm as valid.kara.
package main

import "fmt"

func checkValid(matrix [][]int64) bool {
	n := int64(len(matrix))
	mark := make([]int64, n+1)
	for v := range mark {
		mark[v] = -1
	}
	for i := int64(0); i < n; i++ {
		for j := int64(0); j < n; j++ {
			v := matrix[i][j]
			if mark[v] == 2*i {
				return false
			}
			mark[v] = 2 * i
		}
		for j := int64(0); j < n; j++ {
			v := matrix[j][i]
			if mark[v] == 2*i+1 {
				return false
			}
			mark[v] = 2*i + 1
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func latin(n int64, seed *int64) [][]int64 {
	rows := make([]int64, n)
	symbols := make([]int64, n)
	for i := int64(0); i < n; i++ {
		rows[i] = i
		symbols[i] = i + 1
	}
	for i := n - 1; i >= 1; i-- {
		j := nextRandom(seed) % (i + 1)
		rows[i], rows[j] = rows[j], rows[i]
		j = nextRandom(seed) % (i + 1)
		symbols[i], symbols[j] = symbols[j], symbols[i]
	}
	m := make([][]int64, n)
	for r := int64(0); r < n; r++ {
		m[r] = make([]int64, n)
		for c := int64(0); c < n; c++ {
			m[r][c] = symbols[(rows[r]+c)%n]
		}
	}
	return m
}

func main() {
	seed := int64(2133)
	squares := make([][][]int64, 10)
	for k := range squares {
		squares[k] = latin(100, &seed)
	}
	valid, check := int64(0), int64(0)
	for round := 0; round < 20000; round++ {
		k := nextRandom(&seed) % 10
		r := nextRandom(&seed) % 100
		a := nextRandom(&seed) % 100
		b := nextRandom(&seed) % 100
		var ok bool
		if round%2 == 1 {
			squares[k][a], squares[k][b] = squares[k][b], squares[k][a]
			ok = checkValid(squares[k])
		} else {
			squares[k][r][a], squares[k][r][b] = squares[k][r][b], squares[k][r][a]
			ok = checkValid(squares[k])
			squares[k][r][a], squares[k][r][b] = squares[k][r][b], squares[k][r][a]
		}
		x := int64(0)
		if ok {
			x = 1
		}
		valid += x
		check = (check*31 + x + squares[k][r][a]) % 1000000007
	}
	fmt.Printf("20000 solves: %d valid, checksum %d\n", valid, check)
}
