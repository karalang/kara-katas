// LeetCode #2290: Minimum Obstacle Removal to Reach Corner -- the bench,
// the ★ arm in Go. A 0-1 breadth-first search over a ring-buffer deque: a
// step onto an empty cell to the front, one onto an obstacle to the back.
package main

import (
	"fmt"
	"math"
)

type deque struct {
	buf        [][2]int64
	head, size int
}

func (d *deque) grow() {
	nb := make([][2]int64, len(d.buf)*2+8)
	for i := 0; i < d.size; i++ {
		nb[i] = d.buf[(d.head+i)%len(d.buf)]
	}
	d.buf, d.head = nb, 0
}

func (d *deque) pushFront(x [2]int64) {
	if d.size == len(d.buf) {
		d.grow()
	}
	d.head = (d.head - 1 + len(d.buf)) % len(d.buf)
	d.buf[d.head] = x
	d.size++
}

func (d *deque) pushBack(x [2]int64) {
	if d.size == len(d.buf) {
		d.grow()
	}
	d.buf[(d.head+d.size)%len(d.buf)] = x
	d.size++
}

func (d *deque) popFront() [2]int64 {
	x := d.buf[d.head]
	d.head = (d.head + 1) % len(d.buf)
	d.size--
	return x
}

func minimumObstacles(grid [][]int64) int64 {
	m, n := int64(len(grid)), int64(len(grid[0]))
	cost := make([]int64, m*n)
	best := make([]int64, m*n)
	for i := range cost {
		cost[i] = -1
		best[i] = math.MaxInt64
	}
	q := &deque{}
	best[0] = 0
	q.pushBack([2]int64{0, 0})
	moves := [4][2]int64{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	for q.size > 0 {
		x := q.popFront()
		r, c := x[0], x[1]
		if cost[r*n+c] >= 0 {
			continue
		}
		here := best[r*n+c]
		cost[r*n+c] = here
		if r == m-1 && c == n-1 {
			return here
		}
		for _, mv := range moves {
			nr, nc := r+mv[0], c+mv[1]
			if nr < 0 || nc < 0 || nr >= m || nc >= n {
				continue
			}
			step := grid[nr][nc]
			if here+step < best[nr*n+nc] {
				best[nr*n+nc] = here + step
				if step == 0 {
					q.pushFront([2]int64{nr, nc})
				} else {
					q.pushBack([2]int64{nr, nc})
				}
			}
		}
	}
	return best[m*n-1]
}

var seed int64 = 2290

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int64, 10)
	for g := range grids {
		grid := make([][]int64, 200)
		for r := range grid {
			row := make([]int64, 200)
			for c := range row {
				if nextRandom()%10 < 4 {
					row[c] = 1
				}
			}
			grid[r] = row
		}
		grid[0][0] = 0
		grid[199][199] = 0
		grids[g] = grid
	}
	var check int64
	for p := 0; p < 5; p++ {
		var total int64
		for _, grid := range grids {
			total += minimumObstacles(grid)
		}
		check = (check*31 + total) % 1000000007
	}
	fmt.Printf("5 passes over 10 grids of 200x200: checksum %d\n", check)
}
