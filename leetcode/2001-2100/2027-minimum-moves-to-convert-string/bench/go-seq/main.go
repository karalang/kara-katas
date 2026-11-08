// LeetCode #2027: Minimum Moves to Convert String -- the ★ arm in Go, the
// same algorithm and workload as moves.kara.
package main

import (
	"fmt"
	"strings"
)

func minimumMoves(s string) int64 {
	key := []rune(s)
	var moves int64
	i := 0
	for i < len(key) {
		if key[i] == 'X' {
			moves++
			i += 3
		} else {
			i++
		}
	}
	return moves
}

var seed int64 = 2027

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	all := make([]string, 0, 2000)
	for a := 0; a < 2000; a++ {
		share := nextRandom() % 101
		var sb strings.Builder
		for i := 0; i < 1000; i++ {
			if nextRandom()%100 < share {
				sb.WriteByte('X')
			} else {
				sb.WriteByte('O')
			}
		}
		all = append(all, sb.String())
	}
	var calls, total, check int64
	for r := 0; r < 50; r++ {
		for _, s := range all {
			moves := minimumMoves(s)
			calls++
			total += moves
			check = (check*31 + moves) % 1000000007
		}
	}
	fmt.Printf("%d calls: %d moves, checksum %d\n", calls, total, check)
}
