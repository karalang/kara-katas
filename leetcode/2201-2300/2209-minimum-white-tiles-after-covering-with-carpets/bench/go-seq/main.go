// benchmark's Go mirror of tiles.kara (LeetCode #2209, the ★ arm): a table
// best[j][i], the fewest white tiles left visible among the first i tiles
// with j carpets, filled row by row. The floor is read rune by rune, as
// Kāra's `chars()`.
package main

import (
	"fmt"
	"strings"
)

func minimumWhiteTiles(floor string, numCarpets int, carpetLen int) int64 {
	tiles := []int64{}
	for _, c := range floor {
		if c == '1' {
			tiles = append(tiles, 1)
		} else {
			tiles = append(tiles, 0)
		}
	}
	n := len(tiles)
	best := make([][]int64, numCarpets+1)
	for j := range best {
		best[j] = make([]int64, n+1)
	}
	for j := 0; j <= numCarpets; j++ {
		for i := 1; i <= n; i++ {
			left := best[j][i-1] + tiles[i-1]
			if j == 0 {
				best[j][i] = left
			} else {
				from := i - carpetLen
				if from < 0 {
					from = 0
				}
				best[j][i] = min(left, best[j-1][from])
			}
		}
	}
	return best[numCarpets][n]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2209)
	floors := []string{}
	for f := 0; f < 8; f++ {
		whiteIn8 := int64(f%7 + 1)
		var b strings.Builder
		for i := 0; i < 1000; i++ {
			if nextRandom(&seed)%8 < whiteIn8 {
				b.WriteByte('1')
			} else {
				b.WriteByte('0')
			}
		}
		floors = append(floors, b.String())
	}
	// each floor asked 40 times, carpets 10 to 249, each 1 to 20 long
	check := int64(0)
	for q := 0; q < 40; q++ {
		for f := 0; f < 8; f++ {
			carpets := 10 + (q*37+f*11)%240
			length := 1 + (q*7+f*3)%20
			check = (check*31 + minimumWhiteTiles(floors[f], carpets, length)) % 1000000007
		}
	}
	fmt.Printf("40 passes over 8 floors: checksum %d\n", check)
}
