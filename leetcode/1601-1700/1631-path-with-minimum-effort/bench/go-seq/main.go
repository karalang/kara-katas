// LeetCode #1631: Path With Minimum Effort -- the bench's Go mirror: the ★
// arm on 200 random grids of 100 x 100 heights up to 10^6, all drawn
// first, with container/heap for the queue.
package main

import (
	"container/heap"
	"fmt"
	"math"
)

type entry struct {
	effort int32
	r, c   int64
}

type queue []entry

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	if q[i].effort != q[j].effort {
		return q[i].effort < q[j].effort
	}
	if q[i].r != q[j].r {
		return q[i].r < q[j].r
	}
	return q[i].c < q[j].c
}
func (q queue) Swap(i, j int) { q[i], q[j] = q[j], q[i] }
func (q *queue) Push(x any)   { *q = append(*q, x.(entry)) }
func (q *queue) Pop() any {
	old := *q
	e := old[len(old)-1]
	*q = old[:len(old)-1]
	return e
}

func abs(x int32) int32 {
	if x < 0 {
		return -x
	}
	return x
}

func minimumEffortPath(heights [][]int32) int32 {
	rows, cols := int64(len(heights)), int64(len(heights[0]))
	best := make([][]int32, rows)
	for r := range best {
		best[r] = make([]int32, cols)
		for c := range best[r] {
			best[r][c] = math.MaxInt32
		}
	}
	q := &queue{}
	best[0][0] = 0
	heap.Push(q, entry{0, 0, 0})
	dirs := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for q.Len() > 0 {
		e := heap.Pop(q).(entry)
		if e.r == rows-1 && e.c == cols-1 {
			return e.effort
		}
		if e.effort > best[e.r][e.c] {
			continue
		}
		for _, d := range dirs {
			nr, nc := e.r+d[0], e.c+d[1]
			if nr < 0 || nr >= rows || nc < 0 || nc >= cols {
				continue
			}
			step := max(e.effort, abs(heights[nr][nc]-heights[e.r][e.c]))
			if step < best[nr][nc] {
				best[nr][nc] = step
				heap.Push(q, entry{step, nr, nc})
			}
		}
	}
	return 0
}

var seed int64 = 1631

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int32, 200)
	for g := range grids {
		heights := make([][]int32, 100)
		for r := range heights {
			heights[r] = make([]int32, 100)
			for c := range heights[r] {
				high := nextRandom()
				heights[r][c] = int32((high*32768+nextRandom())%1000000 + 1)
			}
		}
		grids[g] = heights
	}
	var check, total int64
	for _, heights := range grids {
		effort := int64(minimumEffortPath(heights))
		total += effort
		check = (check*31 + effort + 1) % 1000000007
	}
	fmt.Printf("200 grids of 100 x 100: efforts sum to %d, checksum %d\n", total, check)
}
