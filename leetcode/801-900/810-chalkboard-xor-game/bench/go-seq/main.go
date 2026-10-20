// LeetCode 810 -- Chalkboard XOR Game: the bench, with the ★ arm's XOR and
// count.
package main

import "fmt"

var seed int64 = 810

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func xorGame(nums []int64) bool {
	var x int64
	for i := 0; i < len(nums); i++ {
		x ^= nums[i]
	}
	return x == 0 || len(nums)%2 == 0
}

// 64 boards of 999 numbers are made once. Each round writes a new number
// into one place of the next board and asks who wins it.
func main() {
	boards := make([][]int64, 0, 64)
	for k := 0; k < 64; k++ {
		board := make([]int64, 0, 999)
		for i := 0; i < 999; i++ {
			board = append(board, nextRandom())
		}
		boards = append(boards, board)
	}
	var rounds int64 = 10000000
	var wins, check int64
	for r := int64(0); r < rounds; r++ {
		k := r % 64
		boards[k][r/64%999] = nextRandom()
		var win int64
		if xorGame(boards[k]) {
			win = 1
		}
		wins += win
		check = (check*131 + win + r%1000) % 1000000007
	}
	fmt.Printf("%d rounds of 999 numbers: %d won by Alice, checksum %d\n", rounds, wins, check)
}
