// LeetCode #1349 bench -- Go: each row's students as a bit mask,
// best[mask] the most students so far with the last row seated as mask.
package main

import (
	"fmt"
	"math/bits"
)

func maxStudents(seats [][]byte) int {
	n := len(seats[0])
	full := 1 << n
	best := make([]int, full)
	for s := range best {
		best[s] = -1
	}
	best[0] = 0
	for _, row := range seats {
		good := 0
		for j := 0; j < n; j++ {
			if row[j] == '.' {
				good |= 1 << j
			}
		}
		next := make([]int, full)
		for s := range next {
			next[s] = -1
		}
		for mask := 0; mask < full; mask++ {
			if mask&good != mask || mask&(mask<<1) != 0 {
				continue
			}
			here := bits.OnesCount(uint(mask))
			for prev := 0; prev < full; prev++ {
				if best[prev] < 0 || mask&(prev<<1) != 0 || mask&(prev>>1) != 0 {
					continue
				}
				if best[prev]+here > next[mask] {
					next[mask] = best[prev] + here
				}
			}
		}
		best = next
	}
	top := best[0]
	for _, v := range best {
		if v > top {
			top = v
		}
	}
	return top
}

func main() {
	var seed int64 = 1349
	rooms := make([][][]byte, 20)
	for k := range rooms {
		rooms[k] = make([][]byte, 8)
		for i := range rooms[k] {
			rooms[k][i] = make([]byte, 8)
			for j := range rooms[k][i] {
				seed = (seed*1103515245 + 12345) % 2147483648
				if (seed/65536)%4 == 0 {
					rooms[k][i][j] = '#'
				} else {
					rooms[k][i][j] = '.'
				}
			}
		}
	}
	var check int64
	for r := int64(0); r < 3000; r++ {
		k, i, j := check%20, (check/20)%8, (check/160)%8
		if rooms[k][i][j] == '.' {
			rooms[k][i][j] = '#'
		} else {
			rooms[k][i][j] = '.'
		}
		check = (check*31 + int64(maxStudents(rooms[k])) + r) % 1000000007
	}
	fmt.Printf("3000 rounds over 20 rooms of 8 by 8: checksum %d\n", check)
}
