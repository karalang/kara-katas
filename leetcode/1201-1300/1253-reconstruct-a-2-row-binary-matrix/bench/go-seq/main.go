// LeetCode #1253 bench, in Go: the ★ arm (the 2s counted first, then each
// column of 1 giving its 1 to the upper row while it has room, and to the
// lower after) on 20 random cases of 100000 columns built once, each with
// its own share of 2s and half of them with no matrix; each asked 50
// times, every answer folded into a checksum.
package main

import "fmt"

var seed int64 = 1253

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func reconstructMatrix(upper, lower int64, colsum []int64) [][]int64 {
	n := len(colsum)
	var twos, ones int64
	for _, v := range colsum {
		if v == 2 {
			twos++
		}
	}
	for _, v := range colsum {
		if v == 1 {
			ones++
		}
	}
	if upper < twos || lower < twos || upper+lower != 2*twos+ones {
		return [][]int64{}
	}
	up := make([]int64, n)
	low := make([]int64, n)
	left := upper - twos
	for i := 0; i < n; i++ {
		if colsum[i] == 2 {
			up[i] = 1
			low[i] = 1
		} else if colsum[i] == 1 {
			if left > 0 {
				up[i] = 1
				left--
			} else {
				low[i] = 1
			}
		}
	}
	return [][]int64{up, low}
}

type caseT struct {
	upper, lower int64
	colsum       []int64
}

func main() {
	cases := make([]caseT, 0, 20)
	for t := 0; t < 20; t++ {
		twos := nextRandom() % 101
		colsum := make([]int64, 0, 100000)
		var upper, lower int64
		for i := 0; i < 100000; i++ {
			var v int64
			if nextRandom()%100 < twos {
				v = 2
			} else {
				v = nextRandom() % 2
			}
			colsum = append(colsum, v)
			if v == 2 {
				upper++
				lower++
			} else if v == 1 {
				if nextRandom()%2 == 0 {
					upper++
				} else {
					lower++
				}
			}
		}
		if t%2 == 1 {
			upper++
		}
		cases = append(cases, caseT{upper, lower, colsum})
	}
	var check int64
	for r := 0; r < 50; r++ {
		for _, c := range cases {
			ans := reconstructMatrix(c.upper, c.lower, c.colsum)
			var even int64
			if len(ans) > 0 {
				for i := 0; i < len(c.colsum); i += 2 {
					even += ans[0][i]
				}
			}
			check = (check*131 + int64(len(ans)) + even) % 1000000007
		}
	}
	fmt.Printf("50 rounds of 20 cases of 100000 columns: checksum %d\n", check)
}
