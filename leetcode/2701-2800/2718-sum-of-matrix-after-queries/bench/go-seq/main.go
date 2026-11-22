// LeetCode #2718: Sum of Matrix After Queries -- the bench (matrix.kara
// in Go): the queries read from the last back, each row or column not set
// later filling the lines of the other kind not yet taken.
package main

import "fmt"

func matrixSumQueries(n int64, queries [][]int64) int64 {
	rowTaken := make([]bool, n)
	colTaken := make([]bool, n)
	rowsLeft, colsLeft := n, n
	var sum int64
	for k := len(queries) - 1; k >= 0; k-- {
		kind, index, value := queries[k][0], queries[k][1], queries[k][2]
		if kind == 0 {
			if !rowTaken[index] {
				rowTaken[index] = true
				rowsLeft--
				sum += value * colsLeft
			}
		} else if !colTaken[index] {
			colTaken[index] = true
			colsLeft--
			sum += value * rowsLeft
		}
	}
	return sum
}

var seed int64 = 2718

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count, rounds := 40, 20
	const n int64 = 10000
	problems := make([][][]int64, 0, count)
	for c := 0; c < count; c++ {
		queries := make([][]int64, 0, 50000)
		for k := 0; k < 50000; k++ {
			kind := nextRandom() % 2
			index := wide() % n
			value := wide() % 100001
			queries = append(queries, []int64{kind, index, value})
		}
		problems = append(problems, queries)
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, queries := range problems {
			total := matrixSumQueries(n, queries)
			sum += total % 1000000007
			check = (check*31 + total%1000000007 + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d cases of 50000 queries on 10000 rows, %d rounds: sums mod p sum to %d, checksum %d\n", count, rounds, sum, check)
}
