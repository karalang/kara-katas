// Benchmark for #778: Swim in Rising Water -- mirror of the ★ arm
// (Dijkstra on the highest square), with the same workload as the Kāra
// program.
package main

import (
	"container/heap"
	"fmt"
)

type entry struct{ t, at int64 }
type queue []entry

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	return q[i].t < q[j].t || (q[i].t == q[j].t && q[i].at < q[j].at)
}
func (q queue) Swap(i, j int) { q[i], q[j] = q[j], q[i] }
func (q *queue) Push(x any)   { *q = append(*q, x.(entry)) }
func (q *queue) Pop() any {
	old := *q
	e := old[len(old)-1]
	*q = old[:len(old)-1]
	return e
}

var dirs = [4][2]int64{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}

func swimInWater(grid [][]int64) int64 {
	n := int64(len(grid))
	done := make([]bool, n*n)
	q := &queue{{grid[0][0], 0}}
	for q.Len() > 0 {
		e := heap.Pop(q).(entry)
		if done[e.at] {
			continue
		}
		done[e.at] = true
		r, c := e.at/n, e.at%n
		if r == n-1 && c == n-1 {
			return e.t
		}
		for _, d := range dirs {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < n && nc >= 0 && nc < n && !done[nr*n+nc] {
				h := grid[nr][nc]
				if h < e.t {
					h = e.t
				}
				heap.Push(q, entry{h, nr*n + nc})
			}
		}
	}
	return -1
}

var seed int64 = 778

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n = 64, 50
	grids := make([][][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		values := make([]int64, 0, n*n)
		for r := int64(0); r < n; r++ {
			for c := int64(0); c < n; c++ {
				if g%4 == 2 && r%2 == 1 {
					values = append(values, r*n+n-1-c)
				} else {
					values = append(values, r*n+c)
				}
			}
		}
		if g%4 < 2 {
			for i := int64(n*n - 1); i > 0; i-- {
				j := nextRandom() % (i + 1)
				values[i], values[j] = values[j], values[i]
			}
		} else {
			for k := 0; k < 50; k++ {
				i := nextRandom() % (n * n)
				j := nextRandom() % (n * n)
				values[i], values[j] = values[j], values[i]
			}
		}
		grid := make([][]int64, n)
		for r := 0; r < n; r++ {
			grid[r] = append([]int64(nil), values[r*n:(r+1)*n]...)
		}
		grids = append(grids, grid)
	}
	var total, checksum int64
	for round := int64(0); round < 3000; round++ {
		g := (round * 7) % count
		answer := swimInWater(grids[g])
		total += answer
		checksum = (checksum*31 + answer + g) % 1000000007
	}
	fmt.Printf("3000 rounds of 50 x 50 grids: answers sum to %d, checksum %d\n", total, checksum)
}
