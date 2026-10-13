// Benchmark for #474: Go mirror of the ★ arm (0/1 knapsack with two
// budgets, one table); see ../ones_and_zeroes.kara.
package main

import (
	"fmt"
	"strings"
)

func countZeros(s string) int64 {
	var zeros int64
	for _, c := range s {
		if c == '0' {
			zeros++
		}
	}
	return zeros
}

func findMaxForm(strs []string, m, n int64) int64 {
	best := make([][]int64, m+1)
	for i := range best {
		best[i] = make([]int64, n+1)
	}
	for _, s := range strs {
		zeros := countZeros(s)
		ones := int64(len(s)) - zeros
		for i := m; i >= zeros; i-- {
			for j := n; j >= ones; j-- {
				take := best[i-zeros][j-ones] + 1
				if take > best[i][j] {
					best[i][j] = take
				}
			}
		}
	}
	return best[m][n]
}

var seed int64 = 474

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strs := make([]string, 0, 600)
	for k := 0; k < 600; k++ {
		size := 1 + nextRandom()%100
		lean := nextRandom() % 3
		var b strings.Builder
		for i := int64(0); i < size; i++ {
			r := nextRandom() % 4
			var zero bool
			if lean == 0 {
				zero = r != 0
			} else if lean == 1 {
				zero = r == 0
			} else {
				zero = r < 2
			}
			if zero {
				b.WriteByte('0')
			} else {
				b.WriteByte('1')
			}
		}
		strs = append(strs, b.String())
	}
	rounds := 300
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		m := 50 + nextRandom()%51
		n := 50 + nextRandom()%51
		got := findMaxForm(strs, m, n)
		total += got
		checksum = (checksum*31 + got) % 1000000007
	}
	fmt.Printf("%d rounds on 600 strings: %d chosen, checksum %d\n", rounds, total, checksum)
}
