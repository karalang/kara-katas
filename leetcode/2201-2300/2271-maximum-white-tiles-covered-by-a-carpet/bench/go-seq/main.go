// LeetCode #2271: Maximum White Tiles Covered by a Carpet -- the bench,
// the ★ arm.
package main

import (
	"fmt"
	"sort"
)

func maximumWhiteTiles(tiles [][]int64, carpetLen int64) int64 {
	sorted := make([][]int64, len(tiles))
	for i, t := range tiles {
		sorted[i] = []int64{t[0], t[1]}
	}
	sort.Slice(sorted, func(a, b int) bool {
		if sorted[a][0] != sorted[b][0] {
			return sorted[a][0] < sorted[b][0]
		}
		return sorted[a][1] < sorted[b][1]
	})
	m := len(sorted)
	var best, whole int64
	j := 0
	for i := 0; i < m; i++ {
		end := sorted[i][0] + carpetLen - 1
		for j < m && sorted[j][1] <= end {
			whole += sorted[j][1] - sorted[j][0] + 1
			j++
		}
		var part int64
		if j < m && sorted[j][0] <= end {
			part = end - sorted[j][0] + 1
		}
		if whole+part > best {
			best = whole + part
		}
		if j > i {
			whole -= sorted[i][1] - sorted[i][0] + 1
		} else {
			j = i + 1
		}
	}
	return best
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2271

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lens := []int64{1000, 1000000, 1000000000}
	var check int64
	for t := 0; t < 30; t++ {
		tiles := make([][]int64, 0, 50000)
		var at int64 = 1
		for i := 0; i < 50000; i++ {
			at += nextRandom() % 10001
			end := at + nextRandom()%10000
			tiles = append(tiles, []int64{at, end})
			at = end + 1
		}
		for i := 49999; i >= 1; i-- {
			k := nextRandom() % int64(i+1)
			tiles[i], tiles[k] = tiles[k], tiles[i]
		}
		check = (check*31 + maximumWhiteTiles(tiles, lens[t%3])) % 1000000007
	}
	fmt.Printf("30 sets of 5 * 10^4: checksum %d\n", check)
}
