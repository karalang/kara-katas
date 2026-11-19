// LeetCode #1643: Kth Smallest Instructions -- the bench's Go mirror: the
// ★ arm on 1000000 random destinations of 1 to 15 rows and columns, each
// with a k drawn from all of its paths, all drawn first.
package main

import (
	"fmt"
	"strings"
)

func kthSmallestPath(destination []int32, k32 int32) string {
	v, h := int64(destination[0]), int64(destination[1])
	n := v + h
	choose := make([][]int64, n+1)
	for i := range choose {
		choose[i] = make([]int64, n+1)
	}
	for i := int64(0); i <= n; i++ {
		choose[i][0] = 1
		for j := int64(1); j <= i; j++ {
			choose[i][j] = choose[i-1][j-1] + choose[i-1][j]
		}
	}
	k := int64(k32)
	var path strings.Builder
	for s := int64(0); s < n; s++ {
		startingH := choose[h+v-1][v]
		if k <= startingH {
			path.WriteByte('H')
			h--
		} else {
			path.WriteByte('V')
			k -= startingH
			v--
		}
	}
	return path.String()
}

var seed int64 = 1643

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func countPaths(row, column int64) int64 {
	count := int64(1)
	for i := int64(1); i <= row; i++ {
		count = count * (column + i) / i
	}
	return count
}

func main() {
	const cases = 1000000
	drawn := make([][3]int32, cases)
	for c := range drawn {
		row := nextRandom()%15 + 1
		column := nextRandom()%15 + 1
		a := nextRandom()
		b := nextRandom()
		k := (a*32768+b)%countPaths(row, column) + 1
		drawn[c] = [3]int32{int32(row), int32(column), int32(k)}
	}
	var check, total int64
	for _, d := range drawn {
		path := kthSmallestPath(d[:2], d[2])
		total += int64(strings.IndexByte(path, 'V'))
		for i := 0; i < len(path); i++ {
			if path[i] == 'H' {
				check = (check*3 + 1) % 1000000007
			} else {
				check = (check*3 + 2) % 1000000007
			}
		}
	}
	fmt.Printf("%d destinations of up to 15 by 15: first moves down sum to %d, checksum %d\n", cases, total, check)
}
