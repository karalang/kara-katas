// LeetCode #1563: Stone Game V -- bench: the ★ arm (every stretch,
// shortest first, every split) over 5 rows of 400 stones of 1 to 10^6,
// built once, each asked twice.
// Go mirror of stones.kara.
package main

import "fmt"

func stoneGameV(row []int64) int64 {
	n := len(row)
	prefix := make([]int64, n+1)
	for i := 0; i < n; i++ {
		prefix[i+1] = prefix[i] + row[i]
	}
	best := make([][]int64, n)
	for i := range best {
		best[i] = make([]int64, n)
	}
	for length := 2; length <= n; length++ {
		for i := 0; i <= n-length; i++ {
			j := i + length - 1
			var most int64
			for k := i; k < j; k++ {
				left := prefix[k+1] - prefix[i]
				right := prefix[j+1] - prefix[k+1]
				if left < right {
					most = max(most, left+best[i][k])
				} else if left > right {
					most = max(most, right+best[k+1][j])
				} else {
					most = max(most, left+max(best[i][k], best[k+1][j]))
				}
			}
			best[i][j] = most
		}
	}
	return best[0][n-1]
}

var seed int64 = 1563

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	rows := make([][]int64, 5)
	for r := range rows {
		rows[r] = make([]int64, 400)
		for i := range rows[r] {
			v := nextRandom() * 32768
			rows[r][i] = (v+nextRandom())%1000000 + 1
		}
	}
	var check, total int64
	for pass := 0; pass < 2; pass++ {
		for _, row := range rows {
			score := stoneGameV(row)
			total += score
			check = mix(check, score)
		}
	}
	fmt.Printf("2 passes over 5 rows of 400 stones: %d points, checksum %d\n", total, check)
}
