// LeetCode #2151: Maximum Good People Based on Statements -- the
// benchmark's Go mirror of statements.kara.
package main

import (
	"fmt"
	"math/bits"
)

func maximumGood(statements [][]int64) int64 {
	n := len(statements)
	var best int64
	for mask := int64(0); mask < int64(1)<<n; mask++ {
		holds := true
		for i := 0; i < n; i++ {
			if (mask>>i)&1 == 1 {
				for j := 0; j < n; j++ {
					say := statements[i][j]
					if say != 2 && say != (mask>>j)&1 {
						holds = false
					}
				}
			}
		}
		if holds {
			good := int64(bits.OnesCount64(uint64(mask)))
			if good > best {
				best = good
			}
		}
	}
	return best
}

var seed int64 = 2151

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 15
	villages := [][][]int64{}
	for v := 0; v < 4; v++ {
		hidden := nextRandom() % (1 << n)
		statements := [][]int64{}
		for i := int64(0); i < n; i++ {
			row := []int64{}
			for j := int64(0); j < n; j++ {
				var say int64
				if i == j {
					say = 2
				} else if (hidden>>i)&1 == 1 {
					if nextRandom()%3 == 0 {
						say = 2
					} else {
						say = (hidden >> j) & 1
					}
				} else {
					say = nextRandom() % 3
				}
				row = append(row, say)
			}
			statements = append(statements, row)
		}
		villages = append(villages, statements)
	}
	var total, check int64
	for round := int64(0); round < 25; round++ {
		for v := 0; v < 4; v++ {
			i := nextRandom() % n
			j := (i + 1 + nextRandom()%(n-1)) % n
			villages[v][i][j] = nextRandom() % 3
			good := maximumGood(villages[v])
			total += good
			check = (check*31 + good + round) % 1000000007
		}
	}
	fmt.Printf("100 solves: %d good in all, checksum %d\n", total, check)
}
