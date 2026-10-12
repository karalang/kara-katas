// LeetCode #417: Pacific Atlantic Water Flow -- Go mirror of
// pacific_atlantic.kara (search up from each ocean). The queue is a
// slice read from a moving head, Go's usual deque.
package main

import "fmt"

type cell struct{ r, c int64 }

func climb(heights [][]int64, queue []cell) [][]bool {
	rows := int64(len(heights))
	cols := int64(len(heights[0]))
	seen := make([][]bool, rows)
	for r := range seen {
		seen[r] = make([]bool, cols)
	}
	for _, p := range queue {
		seen[p.r][p.c] = true
	}
	dr := [4]int64{-1, 1, 0, 0}
	dc := [4]int64{0, 0, -1, 1}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head].r, queue[head].c
		for k := 0; k < 4; k++ {
			nr := r + dr[k]
			nc := c + dc[k]
			if nr >= 0 && nr < rows && nc >= 0 && nc < cols && !seen[nr][nc] && heights[nr][nc] >= heights[r][c] {
				seen[nr][nc] = true
				queue = append(queue, cell{nr, nc})
			}
		}
	}
	return seen
}

func pacificAtlantic(heights [][]int64) []cell {
	rows := int64(len(heights))
	cols := int64(len(heights[0]))
	var pacific, atlantic []cell
	for r := int64(0); r < rows; r++ {
		pacific = append(pacific, cell{r, 0})
		atlantic = append(atlantic, cell{r, cols - 1})
	}
	for c := int64(0); c < cols; c++ {
		pacific = append(pacific, cell{0, c})
		atlantic = append(atlantic, cell{rows - 1, c})
	}
	toPacific := climb(heights, pacific)
	toAtlantic := climb(heights, atlantic)
	var cells []cell
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if toPacific[r][c] && toAtlantic[r][c] {
				cells = append(cells, cell{r, c})
			}
		}
	}
	return cells
}

var seed int64 = 417

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func ridge(r, c, n int64) int64 {
	a := r + c
	b := 2*n - 2 - r - c
	if a < b {
		return a
	}
	return b
}

func main() {
	var n int64 = 200
	var rounds int64 = 3000
	heights := make([][]int64, n)
	for r := int64(0); r < n; r++ {
		heights[r] = make([]int64, n)
		for c := int64(0); c < n; c++ {
			heights[r][c] = 3*ridge(r, c, n) + step()%3
		}
	}
	var total, checksum int64
	for k := int64(0); k < rounds; k++ {
		r := step() % n
		c := step() % n
		heights[r][c] = step() % (3*ridge(r, c, n) + 3)
		cells := pacificAtlantic(heights)
		total += int64(len(cells))
		last := cells[len(cells)-1]
		checksum = (checksum*31 + int64(len(cells)) + last.r*n + last.c) % 1000000007
	}
	fmt.Printf("%d rounds on a %dx%d grid: %d cells, checksum %d\n", rounds, n, n, total, checksum)
}
