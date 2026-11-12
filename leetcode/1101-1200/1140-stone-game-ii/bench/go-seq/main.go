// LeetCode #1140: Stone Game II -- the bench in Go, the ★ arm's algorithm.
package main

import "fmt"

func stoneGameII(piles []int64) int64 {
	n := int64(len(piles))
	left := make([]int64, n+1)
	for i := n - 1; i >= 0; i-- {
		left[i] = left[i+1] + piles[i]
	}
	best := make([][]int64, n+1)
	for i := range best {
		best[i] = make([]int64, n+1)
	}
	for i := n - 1; i >= 0; i-- {
		for m := int64(1); m <= n; m++ {
			if i+2*m >= n {
				best[i][m] = left[i]
			} else {
				most := int64(0)
				for x := int64(1); x <= 2*m; x++ {
					most = max(most, left[i]-best[i+x][max(m, x)])
				}
				best[i][m] = most
			}
		}
	}
	return best[0][1]
}

var seed int64 = 1140

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rows := make([][]int64, 20)
	for r := range rows {
		rows[r] = make([]int64, 100)
		for i := range rows[r] {
			rows[r][i] = nextRandom()%10000 + 1
		}
	}
	var total, check int64
	for round := 0; round < 100; round++ {
		for r := 0; r < 20; r++ {
			at := nextRandom() % 100
			rows[r][at] = nextRandom()%10000 + 1
			answer := stoneGameII(rows[r])
			total += answer
			check = (check*131 + answer + 1) % 1000000007
		}
	}
	fmt.Printf("100 rounds over 20 rows of 100 piles: answers total %d, checksum %d\n", total, check)
}
