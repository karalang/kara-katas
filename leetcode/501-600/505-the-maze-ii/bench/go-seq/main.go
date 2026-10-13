// Benchmark for #505 in Go: the ★ arm (Dijkstra over the cells the ball
// can stop in); see ../../shortest_distance.kara. container/heap of
// (distance, row, column) triples is the smallest-first queue.
package main

import (
	"container/heap"
	"fmt"
)

type entry struct{ d, r, c int64 }

type queue []entry

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	if q[i].d != q[j].d {
		return q[i].d < q[j].d
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

func shortestDistance(maze [][]int64, start, destination []int64) int64 {
	rows := int64(len(maze))
	cols := int64(len(maze[0]))
	best := make([][]int64, rows)
	for r := range best {
		best[r] = make([]int64, cols)
		for c := range best[r] {
			best[r][c] = -1
		}
	}
	q := &queue{{0, start[0], start[1]}}
	moves := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for q.Len() > 0 {
		e := heap.Pop(q).(entry)
		d, r, c := e.d, e.r, e.c
		if best[r][c] != -1 {
			continue
		}
		best[r][c] = d
		if r == destination[0] && c == destination[1] {
			return d
		}
		for _, m := range moves {
			dr, dc := m[0], m[1]
			nr, nc, steps := r, c, int64(0)
			for nr+dr >= 0 && nr+dr < rows && nc+dc >= 0 && nc+dc < cols && maze[nr+dr][nc+dc] == 0 {
				nr += dr
				nc += dc
				steps++
			}
			if steps > 0 && best[nr][nc] == -1 {
				heap.Push(q, entry{d + steps, nr, nc})
			}
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 2,000 mazes of 100 by 100 (the problem's most), a wall in each
	// cell with odds of 1 in 4, with a start and a destination in two
	// different open cells, built once. Then each is solved once.
	mazes := 2000
	seed := int64(505)
	var all [][][]int64
	var starts, destinations [][]int64
	for k := 0; k < mazes; k++ {
		var maze [][]int64
		var open [][2]int64
		for r := int64(0); r < 100; r++ {
			var line []int64
			for c := int64(0); c < 100; c++ {
				if nextRandom(&seed)%4 == 0 {
					line = append(line, 1)
				} else {
					line = append(line, 0)
					open = append(open, [2]int64{r, c})
				}
			}
			maze = append(maze, line)
		}
		n := int64(len(open))
		a := nextRandom(&seed) % n
		b := nextRandom(&seed) % (n - 1)
		if b >= a {
			b++
		}
		starts = append(starts, []int64{open[a][0], open[a][1]})
		destinations = append(destinations, []int64{open[b][0], open[b][1]})
		all = append(all, maze)
	}
	var reached, total, checksum int64
	for k := 0; k < mazes; k++ {
		d := shortestDistance(all[k], starts[k], destinations[k])
		if d != -1 {
			reached++
			total += d
		}
		checksum = (checksum*31 + d + 1) % 1000000007
	}
	fmt.Printf("%d mazes of 100 by 100: the destination reached in %d, distance %d in all, checksum %d\n", mazes, reached, total, checksum)
}
