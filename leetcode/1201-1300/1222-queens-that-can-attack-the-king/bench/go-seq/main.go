// LeetCode #1222 bench, Go mirror of the Kāra ★ arm: mark the queens on an
// 8 by 8 board, then walk out from the king in each of the eight
// directions, over 5000 random boards of 1 to 63 queens drawn once, 50
// passes; checksum of the attackers in the order found.
package main

import "fmt"

var seed int64 = 1222

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func queensAttacktheKing(queens [][]int64, king []int64) [][]int64 {
	var board [8][8]bool
	for _, q := range queens {
		board[q[0]][q[1]] = true
	}
	attackers := [][]int64{}
	for dx := int64(-1); dx <= 1; dx++ {
		for dy := int64(-1); dy <= 1; dy++ {
			if dx == 0 && dy == 0 {
				continue
			}
			x, y := king[0]+dx, king[1]+dy
			for x >= 0 && x < 8 && y >= 0 && y < 8 {
				if board[x][y] {
					attackers = append(attackers, []int64{x, y})
					break
				}
				x += dx
				y += dy
			}
		}
	}
	return attackers
}

type board struct {
	queens [][]int64
	king   []int64
}

func main() {
	boards := make([]board, 0, 5000)
	for i := 0; i < 5000; i++ {
		count := nextRandom()%63 + 1
		squares := make([]int64, 64)
		for k := range squares {
			squares[k] = int64(k)
		}
		for k := int64(0); k < count+1; k++ {
			j := k + nextRandom()%(64-k)
			squares[k], squares[j] = squares[j], squares[k]
		}
		queens := make([][]int64, count)
		for k := int64(0); k < count; k++ {
			queens[k] = []int64{squares[k] / 8, squares[k] % 8}
		}
		boards = append(boards, board{queens, []int64{squares[count] / 8, squares[count] % 8}})
	}
	var total, check int64
	for pass := 0; pass < 200; pass++ {
		for _, b := range boards {
			attackers := queensAttacktheKing(b.queens, b.king)
			total += int64(len(attackers))
			for _, a := range attackers {
				check = (check*131 + a[0]*8 + a[1] + 1) % 1000000007
			}
		}
	}
	fmt.Printf("5000 boards of 1 to 63 queens, 200 passes: attackers total %d, checksum %d\n", total, check)
}
