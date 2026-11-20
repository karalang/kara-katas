// LeetCode #1246 bench, in Go: the ★ arm (interval dynamic programming,
// rows from the last) on 1000 random arrays of 100 values built once, each
// from 1 to v distinct values with v from 1 to 20, each asked twice; every
// answer folded into a checksum.
package main

import "fmt"

func minimumMoves(arr []int64) int64 {
	n := len(arr)
	best := make([][]int64, n+1)
	for i := range best {
		best[i] = make([]int64, n+1)
	}
	for i := n - 1; i >= 0; i-- {
		for j := i + 1; j <= n; j++ {
			moves := 1 + best[i+1][j]
			if i+1 < j && arr[i+1] == arr[i] && 1+best[i+2][j] < moves {
				moves = 1 + best[i+2][j]
			}
			for k := i + 2; k < j; k++ {
				if arr[k] == arr[i] && best[i+1][k]+best[k+1][j] < moves {
					moves = best[i+1][k] + best[k+1][j]
				}
			}
			best[i][j] = moves
		}
	}
	return best[0][n]
}

var seed int64 = 1246

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 1000)
	for a := 0; a < 1000; a++ {
		values := nextRandom()%20 + 1
		arr := make([]int64, 100)
		for i := range arr {
			arr[i] = nextRandom()%values + 1
		}
		arrays = append(arrays, arr)
	}
	var check int64
	for r := 0; r < 2; r++ {
		for _, arr := range arrays {
			check = (check*131 + minimumMoves(arr)) % 1000000007
		}
	}
	fmt.Printf("2 rounds of 1000 arrays of 100 values: checksum %d\n", check)
}
