// LeetCode #2038: Remove Colored Pieces if Both Neighbors are the Same
// Color -- the ★ arm in Go, the same algorithm and workload as colors.kara:
// each row written out as a fresh string, its pieces read as runes, each
// player's moves counted, Alice winning with more.
package main

import "fmt"

func winnerOfGame(colors string) bool {
	c := []rune(colors)
	var alice, bob int64
	for i := 1; i+1 < len(c); i++ {
		if c[i-1] == c[i] && c[i] == c[i+1] {
			if c[i] == 'A' {
				alice++
			} else {
				bob++
			}
		}
	}
	return alice > bob
}

var seed int64 = 2038

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	stays := []int64{2, 3, 50, 1000}
	rows := make([][]rune, 4)
	for r := 0; r < 4; r++ {
		c := 'B'
		if nextRandom()%2 == 0 {
			c = 'A'
		}
		row := make([]rune, 0, 100000)
		for i := 0; i < 100000; i++ {
			if nextRandom()%stays[r] == 0 {
				if c == 'A' {
					c = 'B'
				} else {
					c = 'A'
				}
			}
			row = append(row, c)
		}
		rows[r] = row
	}
	var calls, wins, check int64
	for round := int64(0); round < 100; round++ {
		for r := int64(0); r < 4; r++ {
			at := (round*7919 + r*104729) % 100000
			if rows[r][at] == 'A' {
				rows[r][at] = 'B'
			} else {
				rows[r][at] = 'A'
			}
			var bit int64
			if winnerOfGame(string(rows[r])) {
				bit = 1
			}
			calls++
			wins += bit
			check = (check*3 + bit + 1) % 1000000007
		}
	}
	fmt.Printf("%d calls: Alice wins %d, checksum %d\n", calls, wins, check)
}
