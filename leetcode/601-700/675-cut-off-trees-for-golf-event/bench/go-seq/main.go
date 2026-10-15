// Benchmark for #675: a breadth-first search for each walk, as the Kara
// ★ arm.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 675

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

var moves = [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}

func steps(forest [][]int64, sr, sc, tr, tc int64) int64 {
	if sr == tr && sc == tc {
		return 0
	}
	rows := int64(len(forest))
	cols := int64(len(forest[0]))
	seen := make([]bool, rows*cols)
	queue := make([]int64, 0)
	queue = append(queue, sr*cols+sc)
	seen[sr*cols+sc] = true
	head := 0
	var dist int64
	for head < len(queue) {
		end := len(queue)
		dist++
		for head < end {
			cell := queue[head]
			head++
			r := cell / cols
			c := cell % cols
			for _, m := range moves {
				nr := r + m[0]
				nc := c + m[1]
				if nr >= 0 && nr < rows && nc >= 0 && nc < cols && forest[nr][nc] != 0 && !seen[nr*cols+nc] {
					if nr == tr && nc == tc {
						return dist
					}
					seen[nr*cols+nc] = true
					queue = append(queue, nr*cols+nc)
				}
			}
		}
	}
	return -1
}

type tree struct{ height, r, c int64 }

func cutOffTree(forest [][]int64) int64 {
	trees := make([]tree, 0)
	for r := range forest {
		for c := range forest[0] {
			if forest[r][c] > 1 {
				trees = append(trees, tree{forest[r][c], int64(r), int64(c)})
			}
		}
	}
	sort.Slice(trees, func(a, b int) bool { return trees[a].height < trees[b].height })
	var total, r, c int64
	for _, t := range trees {
		d := steps(forest, r, c, t.r, t.c)
		if d < 0 {
			return -1
		}
		total += d
		r = t.r
		c = t.c
	}
	return total
}

func randomForest(rows, cols, walls, trees int64) [][]int64 {
	forest := make([][]int64, 0)
	spots := make([]int64, 0)
	for r := int64(0); r < rows; r++ {
		row := make([]int64, 0)
		for c := int64(0); c < cols; c++ {
			k := nextRandom() % 100
			if (r > 0 || c > 0) && k < walls {
				row = append(row, 0)
			} else {
				row = append(row, 1)
				if k < walls+trees {
					spots = append(spots, r*cols+c)
				}
			}
		}
		forest = append(forest, row)
	}
	i := int64(len(spots))
	for i > 1 {
		j := nextRandom() % i
		i--
		spots[i], spots[j] = spots[j], spots[i]
	}
	for k := range spots {
		forest[spots[k]/cols][spots[k]%cols] = 2 + int64(k)*7
	}
	return forest
}

func main() {
	forests := 40
	var sum int64
	reached := 0
	for f := 0; f < forests; f++ {
		forest := randomForest(50, 50, 10, 30)
		got := cutOffTree(forest)
		if got >= 0 {
			reached++
		}
		sum = (sum*31 + got + 1) % 1000000007
	}
	fmt.Printf("%d forests of 50x50, %d reachable: checksum %d\n", forests, reached, sum)
}
