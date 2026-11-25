// LeetCode #1368 bench -- Go: a 0-1 breadth-first search over the cells,
// a step the sign points to costing 0 and going to the front of the
// deque, any other costing 1 and going to its back.
package main

import (
	"fmt"
	"math"
)

var moves = [4][2]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}

// deque is a ring buffer of cell indices that grows as needed
type deque struct {
	ring      []int
	head, len int
}

func (q *deque) grow() {
	bigger := make([]int, len(q.ring)*2)
	for i := 0; i < q.len; i++ {
		bigger[i] = q.ring[(q.head+i)%len(q.ring)]
	}
	q.ring, q.head = bigger, 0
}

func (q *deque) pushFront(x int) {
	if q.len == len(q.ring) {
		q.grow()
	}
	q.head = (q.head + len(q.ring) - 1) % len(q.ring)
	q.ring[q.head] = x
	q.len++
}

func (q *deque) pushBack(x int) {
	if q.len == len(q.ring) {
		q.grow()
	}
	q.ring[(q.head+q.len)%len(q.ring)] = x
	q.len++
}

func (q *deque) popFront() int {
	x := q.ring[q.head]
	q.head = (q.head + 1) % len(q.ring)
	q.len--
	return x
}

func minCost(grid [][]int32) int32 {
	m, n := len(grid), len(grid[0])
	cost := make([][]int32, m)
	for r := range cost {
		cost[r] = make([]int32, n)
		for c := range cost[r] {
			cost[r][c] = math.MaxInt32
		}
	}
	q := &deque{ring: make([]int, 1024)}
	cost[0][0] = 0
	q.pushBack(0)
	for q.len > 0 {
		at := q.popFront()
		r, c := at/n, at%n
		for d := 0; d < 4; d++ {
			nr, nc := r+moves[d][0], c+moves[d][1]
			if nr < 0 || nr >= m || nc < 0 || nc >= n {
				continue
			}
			step := int32(1)
			if grid[r][c] == int32(d+1) {
				step = 0
			}
			if cost[r][c]+step < cost[nr][nc] {
				cost[nr][nc] = cost[r][c] + step
				if step == 0 {
					q.pushFront(nr*n + nc)
				} else {
					q.pushBack(nr*n + nc)
				}
			}
		}
	}
	return cost[m-1][n-1]
}

var seed int64 = 1368

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 grids of 100 by 100 signs, the constraints' most, built once;
	// then 600 rounds, each changing one cell's sign and finding the
	// cheapest valid path through that grid, all drawn from the checksum
	// so far
	grids := make([][][]int32, 20)
	for g := range grids {
		grid := make([][]int32, 100)
		for r := range grid {
			grid[r] = make([]int32, 100)
			for c := range grid[r] {
				grid[r][c] = int32(1 + nextRandom()%4)
			}
		}
		grids[g] = grid
	}
	var check int64
	for r := int64(0); r < 600; r++ {
		g := check % 20
		cell := (check / 20) % 10000
		grids[g][cell/100][cell%100] = int32(1 + (check/200000)%4)
		cost := int64(minCost(grids[g]))
		check = (check*31 + cost + r) % 1000000007
	}
	fmt.Printf("600 rounds over 20 grids of 100 by 100: checksum %d\n", check)
}
