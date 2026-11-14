// LeetCode #1536: Minimum Swaps to Arrange a Binary Grid -- bench: the ★
// arm over 50 random 200 x 200 grids, built once and answered 50 times.
// Go mirror of swaps.kara.
package main

import "fmt"

func minSwaps(grid [][]int64) int64 {
	n := len(grid)
	zeros := make([]int, 0, n)
	for _, row := range grid {
		count := 0
		for count < n && row[n-1-count] == 0 {
			count++
		}
		zeros = append(zeros, count)
	}
	var swaps int64
	for i := 0; i < n; i++ {
		need := n - 1 - i
		j := i
		for j < n && zeros[j] < need {
			j++
		}
		if j == n {
			return -1
		}
		for j > i {
			zeros[j], zeros[j-1] = zeros[j-1], zeros[j]
			j--
			swaps++
		}
	}
	return swaps
}

var seed int64 = 1536

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func grid(n int64) [][]int64 {
	zeros := make([]int64, n)
	for i := range zeros {
		zeros[i] = int64(i)
	}
	if nextRandom()%2 == 0 {
		for i := n - 1; i >= 1; i-- {
			j := nextRandom() % (i + 1)
			zeros[i], zeros[j] = zeros[j], zeros[i]
		}
		for i := range zeros {
			z := zeros[i] + nextRandom()%2
			if z > n {
				z = n
			}
			zeros[i] = z
		}
	} else {
		for i := range zeros {
			zeros[i] = nextRandom() % (n + 1)
		}
	}
	rows := make([][]int64, n)
	for i := range rows {
		row := make([]int64, n)
		if zeros[i] < n {
			row[n-1-zeros[i]] = 1
			for c := int64(0); c < n-1-zeros[i]; c++ {
				row[c] = nextRandom() % 2
			}
		}
		rows[i] = row
	}
	return rows
}

func main() {
	grids := make([][][]int64, 50)
	for p := range grids {
		grids[p] = grid(200)
	}
	var check int64
	for pass := 0; pass < 50; pass++ {
		for _, g := range grids {
			check = mix(check, minSwaps(g)+1)
		}
	}
	fmt.Printf("50 passes over 50 grids of 200 rows: checksum %d\n", check)
}
