// LeetCode 749 — Contain Virus, bench: the ★ arm (flood fill each day)
// on a 50 x 50 grid that keeps changing. Mirrors contain_virus.kara.
package main

import "fmt"

func containVirus(isInfected [][]int64) int64 {
	m, n := len(isInfected), len(isInfected[0])
	// 0 clean, 1 infected, 2 walled off
	g := make([]int64, 0, m*n)
	for _, row := range isInfected {
		g = append(g, row...)
	}
	var walls int64
	for {
		region := make([]int, m*n)
		mark := make([]int, m*n)
		for i := range region {
			region[i] = -1
			mark[i] = -1
		}
		var cells, threats [][]int
		var needs []int64
		for start := 0; start < m*n; start++ {
			if g[start] != 1 || region[start] != -1 {
				continue
			}
			id := len(cells)
			var mine, threat []int
			var need int64
			stack := []int{start}
			region[start] = id
			for len(stack) > 0 {
				at := stack[len(stack)-1]
				stack = stack[:len(stack)-1]
				mine = append(mine, at)
				r, c := at/n, at%n
				var next []int
				if r > 0 {
					next = append(next, at-n)
				}
				if r < m-1 {
					next = append(next, at+n)
				}
				if c > 0 {
					next = append(next, at-1)
				}
				if c < n-1 {
					next = append(next, at+1)
				}
				for _, y := range next {
					if g[y] == 0 {
						need++
						if mark[y] != id {
							mark[y] = id
							threat = append(threat, y)
						}
					} else if g[y] == 1 && region[y] == -1 {
						region[y] = id
						stack = append(stack, y)
					}
				}
			}
			cells = append(cells, mine)
			threats = append(threats, threat)
			needs = append(needs, need)
		}
		best := -1
		for id := range cells {
			if len(threats[id]) > 0 && (best == -1 || len(threats[id]) > len(threats[best])) {
				best = id
			}
		}
		if best == -1 {
			break
		}
		walls += needs[best]
		for id := range cells {
			if id == best {
				for _, x := range cells[id] {
					g[x] = 2
				}
			} else {
				for _, x := range threats[id] {
					g[x] = 1
				}
			}
		}
	}
	return walls
}

var seed int64 = 749

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds = 3000
	grid := make([][]int64, 50)
	for r := range grid {
		grid[r] = make([]int64, 50)
		for c := range grid[r] {
			if nextRandom()%100 < 5 {
				grid[r][c] = 1
			}
		}
	}
	var total, check int64
	for round := 0; round < rounds; round++ {
		for k := 0; k < 20; k++ {
			r := nextRandom() % 50
			c := nextRandom() % 50
			if nextRandom()%100 < 5 {
				grid[r][c] = 1
			} else {
				grid[r][c] = 0
			}
		}
		w := containVirus(grid)
		total += w
		check = (check*31 + w) % 1000000007
	}
	fmt.Printf("%d grids of 50 x 50: %d walls in all, checksum %d\n", rounds, total, check)
}
