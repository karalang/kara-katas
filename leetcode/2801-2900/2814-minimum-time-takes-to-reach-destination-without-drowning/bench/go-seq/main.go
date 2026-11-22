// LeetCode #2814: Minimum Time Takes to Reach Destination Without
// Drowning -- the bench in Go: the ★ arm over 200 lands of 100 by 100, a
// cell in five stone and one in 5000 flooded, all drawn first, then each
// answered 5 times. The land is a [][]string as in Kāra; the queues are
// slices read from a head index.
package main

import (
	"fmt"
	"math"
)

var dirs = [4][2]int64{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}

type cell struct{ r, c int64 }

func minimumSeconds(land [][]string) int64 {
	n, m := int64(len(land)), int64(len(land[0]))
	flood := make([][]int64, n)
	time := make([][]int64, n)
	queue := []cell{}
	for r := int64(0); r < n; r++ {
		flood[r] = make([]int64, m)
		time[r] = make([]int64, m)
		for c := int64(0); c < m; c++ {
			flood[r][c] = math.MaxInt64
			time[r][c] = -1
			if land[r][c] == "*" {
				flood[r][c] = 0
				queue = append(queue, cell{r, c})
			}
		}
	}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head].r, queue[head].c
		for _, d := range dirs {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < n && nc >= 0 && nc < m && flood[nr][nc] == math.MaxInt64 &&
				(land[nr][nc] == "." || land[nr][nc] == "S") {
				flood[nr][nc] = flood[r][c] + 1
				queue = append(queue, cell{nr, nc})
			}
		}
	}
	queue = queue[:0]
	for r := int64(0); r < n; r++ {
		for c := int64(0); c < m; c++ {
			if land[r][c] == "S" {
				time[r][c] = 0
				queue = append(queue, cell{r, c})
			}
		}
	}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head].r, queue[head].c
		if land[r][c] == "D" {
			return time[r][c]
		}
		for _, d := range dirs {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < n && nc >= 0 && nc < m && time[nr][nc] == -1 && land[nr][nc] != "X" &&
				flood[nr][nc] > time[r][c]+1 {
				time[nr][nc] = time[r][c] + 1
				queue = append(queue, cell{nr, nc})
			}
		}
	}
	return -1
}

var seed int64 = 2814

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 200, 5
	var n int64 = 100
	lands := make([][][]string, count)
	for g := range lands {
		land := make([][]string, n)
		for r := range land {
			land[r] = make([]string, n)
			for c := range land[r] {
				roll := nextRandom() % 10000
				if roll < 2000 {
					land[r][c] = "X"
				} else if roll < 2002 {
					land[r][c] = "*"
				} else {
					land[r][c] = "."
				}
			}
		}
		start := nextRandom() % (n * n)
		end := nextRandom() % (n*n - 1)
		if end >= start {
			end++
		}
		land[start/n][start%n] = "S"
		land[end/n][end%n] = "D"
		lands[g] = land
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, land := range lands {
			a := minimumSeconds(land)
			total += a
			check = (check*31 + a + 2 + r) % 1000000007
		}
	}
	fmt.Printf("%d lands of %d by %d, %d rounds: seconds sum to %d, checksum %d\n", count, n, n, rounds, total, check)
}
