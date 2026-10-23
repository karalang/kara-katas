// LeetCode #877 bench: Go mirror of stone_game.kara (the ★ arm, the best
// margin of every run of piles) on the same 1,000 games.
package main

import "fmt"

func stoneGame(piles []int64) bool {
	n := len(piles)
	margin := make([][]int64, n)
	for i := range margin {
		margin[i] = make([]int64, n)
		margin[i][i] = piles[i]
	}
	for length := 2; length <= n; length++ {
		for i := 0; i+length <= n; i++ {
			j := i + length - 1
			left := piles[i] - margin[i+1][j]
			right := piles[j] - margin[i][j-1]
			if left > right {
				margin[i][j] = left
			} else {
				margin[i][j] = right
			}
		}
	}
	return margin[0][n-1] > 0
}

var seed int64 = 877

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomPiles(limit int64) []int64 {
	piles := make([]int64, 500)
	var total int64
	for i := range piles {
		piles[i] = nextRandom()%limit + 1
		total += piles[i]
	}
	if total%2 == 0 {
		if piles[0] == limit {
			piles[0]--
		} else {
			piles[0]++
		}
	}
	return piles
}

func main() {
	rows := make([][]int64, 20)
	for k := range rows {
		limit := int64(3)
		if k%2 == 0 {
			limit = 500
		}
		rows[k] = randomPiles(limit)
	}
	var wins, check int64
	for k := 0; k < 1000; k++ {
		answer := stoneGame(rows[k%20])
		a := int64(2)
		if answer {
			wins++
			a = 1
		}
		check = (check*3 + a) % 1000000007
	}
	fmt.Printf("1000 games of 500 piles: Alice wins %d, checksum %d\n", wins, check)
}
