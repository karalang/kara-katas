// Benchmark for #499: Go mirror of the ★ arm (Dijkstra over the places
// the ball stops); see ../the_maze_iii.kara. The queue is a
// container/heap ordered by (distance, instructions), least first.
package main

import (
	"container/heap"
	"fmt"
)

type entry struct {
	dist     int64
	path     string
	row, col int
}

type queue []entry

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	if q[i].dist != q[j].dist {
		return q[i].dist < q[j].dist
	}
	if q[i].path != q[j].path {
		return q[i].path < q[j].path
	}
	if q[i].row != q[j].row {
		return q[i].row < q[j].row
	}
	return q[i].col < q[j].col
}
func (q queue) Swap(i, j int) { q[i], q[j] = q[j], q[i] }
func (q *queue) Push(x any)   { *q = append(*q, x.(entry)) }
func (q *queue) Pop() any {
	old := *q
	e := old[len(old)-1]
	*q = old[:len(old)-1]
	return e
}

type move struct {
	dr, dc int
	name   string
}

func findShortestWay(maze [][]int64, ball, hole []int) string {
	rows := len(maze)
	cols := len(maze[0])
	moves := []move{{1, 0, "d"}, {0, -1, "l"}, {0, 1, "r"}, {-1, 0, "u"}}
	done := make([][]bool, rows)
	for i := range done {
		done[i] = make([]bool, cols)
	}
	q := &queue{{0, "", ball[0], ball[1]}}
	for q.Len() > 0 {
		e := heap.Pop(q).(entry)
		if done[e.row][e.col] {
			continue
		}
		done[e.row][e.col] = true
		if e.row == hole[0] && e.col == hole[1] {
			return e.path
		}
		for _, m := range moves {
			r, c := e.row, e.col
			var steps int64
			for r+m.dr >= 0 && r+m.dr < rows && c+m.dc >= 0 && c+m.dc < cols && maze[r+m.dr][c+m.dc] == 0 {
				r += m.dr
				c += m.dc
				steps++
				if r == hole[0] && c == hole[1] {
					break
				}
			}
			if steps > 0 && !done[r][c] {
				heap.Push(q, entry{e.dist + steps, e.path + m.name, r, c})
			}
		}
	}
	return "impossible"
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 1,000 mazes of 100 by 100 (the problem's most), a wall in each
	// cell with odds of 1 in 4, with a ball and a hole in two different
	// open cells, built once. Then each is solved once.
	mazes := 1000
	var seed int64 = 499
	all := [][][]int64{}
	balls := [][]int{}
	holes := [][]int{}
	for k := 0; k < mazes; k++ {
		maze := [][]int64{}
		open := [][2]int{}
		for r := 0; r < 100; r++ {
			line := []int64{}
			for c := 0; c < 100; c++ {
				if nextRandom(&seed)%4 == 0 {
					line = append(line, 1)
				} else {
					line = append(line, 0)
					open = append(open, [2]int{r, c})
				}
			}
			maze = append(maze, line)
		}
		a := nextRandom(&seed) % int64(len(open))
		b := nextRandom(&seed) % int64(len(open)-1)
		if b >= a {
			b++
		}
		balls = append(balls, []int{open[a][0], open[a][1]})
		holes = append(holes, []int{open[b][0], open[b][1]})
		all = append(all, maze)
	}
	reached := 0
	letters := 0
	var checksum int64
	for k := 0; k < mazes; k++ {
		way := findShortestWay(all[k], balls[k], holes[k])
		if way != "impossible" {
			reached++
			letters += len(way)
		}
		for _, ch := range way {
			checksum = (checksum*31 + int64(ch)) % 1000000007
		}
	}
	fmt.Printf("%d mazes of 100 by 100: the hole reached in %d, %d instructions in all, checksum %d\n", mazes, reached, letters, checksum)
}
