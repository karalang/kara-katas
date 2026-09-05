// Benchmark lane for LeetCode 317 — Go mirror of bench/shortest_distance.kara.
// Build the grid once (20% obstacles, BUILDINGS buildings on corner-reachable
// empty cells), then PASSES one-BFS-per-building passes, each after relocating
// one building to an empty cell chosen from the checksum (moved back after).
package main

import "fmt"

const (
	ROWS         = 360
	COLS         = 360
	BUILDINGS    = 20
	OBSTACLE_PCT = 20
	PASSES       = 30
	MASK         = 1073741823
)

func lcg(s int64) int64 {
	return (s*1103515245 + 12345) & 0x7fffffff
}

func shortestDistance(grid []int64, rows, cols int64) int64 {
	n := int(rows * cols)
	total := make([]int64, n)
	reach := make([]int64, n)
	seen := make([]int64, n)
	dist := make([]int64, n)
	var b int64 = 0
	for src := 0; src < n; src++ {
		if grid[src] != 1 {
			continue
		}
		b++
		seen[src] = b
		dist[src] = 0
		q := make([]int, 0)
		q = append(q, src)
		head := 0
		for head < len(q) {
			cell := q[head]
			head++
			r := int64(cell) / cols
			c := int64(cell) % cols
			d := dist[cell] + 1
			visit := func(nb int) {
				if grid[nb] == 0 && seen[nb] != b {
					seen[nb] = b
					dist[nb] = d
					total[nb] += d
					reach[nb]++
					q = append(q, nb)
				}
			}
			if r > 0 {
				visit(cell - int(cols))
			}
			if r < rows-1 {
				visit(cell + int(cols))
			}
			if c > 0 {
				visit(cell - 1)
			}
			if c < cols-1 {
				visit(cell + 1)
			}
		}
	}
	var best int64 = -1
	for i := 0; i < n; i++ {
		if grid[i] == 0 && reach[i] == b && (best < 0 || total[i] < best) {
			best = total[i]
		}
	}
	return best
}

func main() {
	n := ROWS * COLS
	var seed int64 = 317
	grid := make([]int64, n)
	for i := 0; i < n; i++ {
		seed = lcg(seed)
		if (seed/65536)%100 < OBSTACLE_PCT {
			grid[i] = 2
		} else {
			grid[i] = 0
		}
	}
	grid[0] = 0

	reachable := make([]bool, n)
	q := make([]int, 0)
	reachable[0] = true
	q = append(q, 0)
	head := 0
	for head < len(q) {
		cell := q[head]
		head++
		r := cell / COLS
		c := cell % COLS
		if r > 0 && grid[cell-COLS] != 2 && !reachable[cell-COLS] {
			reachable[cell-COLS] = true
			q = append(q, cell-COLS)
		}
		if r < ROWS-1 && grid[cell+COLS] != 2 && !reachable[cell+COLS] {
			reachable[cell+COLS] = true
			q = append(q, cell+COLS)
		}
		if c > 0 && grid[cell-1] != 2 && !reachable[cell-1] {
			reachable[cell-1] = true
			q = append(q, cell-1)
		}
		if c < COLS-1 && grid[cell+1] != 2 && !reachable[cell+1] {
			reachable[cell+1] = true
			q = append(q, cell+1)
		}
	}

	sites := make([]int, 0, BUILDINGS)
	for len(sites) < BUILDINGS {
		seed = lcg(seed)
		p := int((seed / 256) % int64(n))
		if grid[p] == 0 && reachable[p] {
			grid[p] = 1
			sites = append(sites, p)
		}
	}

	var checksum int64 = 0
	for pass := 0; pass < PASSES; pass++ {
		old := sites[pass%BUILDINGS]
		i := int(checksum % int64(n))
		for grid[i] != 0 {
			i = (i + 1) % n
		}
		grid[old] = 0
		grid[i] = 1
		ans := shortestDistance(grid, ROWS, COLS)
		checksum = (checksum*31 + ans + 7) & MASK
		grid[i] = 0
		grid[old] = 1
	}
	fmt.Printf("checksum %d\n", checksum)
}
