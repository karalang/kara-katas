// LeetCode #1263 bench, in Go: the ★ arm's 0-1 BFS over (box, player)
// states (a step to the front of a ring-buffer deque, a push to the back,
// a state final the first time it leaves) on 100 random 20 by 20 grids, a
// cell in 10 a wall, built once, 20 rounds; every answer folded into a
// checksum. Each state enters the deque at most 4 times, so a ring of
// 2^20 entries never fills.
package main

import "fmt"

const ring = 1 << 20

type state struct{ b, p, pushes int64 }

func minPushBox(grid [][]byte, buf []state) int64 {
	m := int64(len(grid))
	n := int64(len(grid[0]))
	var player, boxAt, target int64
	for r := int64(0); r < m; r++ {
		for c := int64(0); c < n; c++ {
			switch grid[r][c] {
			case 'S':
				player = r*n + c
			case 'B':
				boxAt = r*n + c
			case 'T':
				target = r*n + c
			}
		}
	}
	cells := m * n
	done := make([]bool, cells*cells)
	head, length := 0, 1
	buf[0] = state{boxAt, player, 0}
	dirs := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for length > 0 {
		s := buf[head]
		head = (head + 1) & (ring - 1)
		length--
		if done[s.b*cells+s.p] {
			continue
		}
		done[s.b*cells+s.p] = true
		if s.b == target {
			return s.pushes
		}
		for _, d := range dirs {
			dr, dc := d[0], d[1]
			r := s.p/n + dr
			c := s.p%n + dc
			if r < 0 || r >= m || c < 0 || c >= n || grid[r][c] == '#' {
				continue
			}
			q := r*n + c
			if q != s.b {
				head = (head - 1) & (ring - 1)
				buf[head] = state{s.b, q, s.pushes}
				length++
				continue
			}
			br, bc := r+dr, c+dc
			if br >= 0 && br < m && bc >= 0 && bc < n && grid[br][bc] != '#' {
				buf[(head+length)&(ring-1)] = state{br*n + bc, q, s.pushes + 1}
				length++
			}
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func isMark(ch byte) bool { return ch == 'S' || ch == 'B' || ch == 'T' }

func randomGrid(m, n, walls int64, seed *int64) [][]byte {
	grid := make([][]byte, m)
	for r := range grid {
		grid[r] = make([]byte, n)
		for c := range grid[r] {
			if nextRandom(seed)%walls == 0 {
				grid[r][c] = '#'
			} else {
				grid[r][c] = '.'
			}
		}
	}
	for _, mark := range []byte{'S', 'B', 'T'} {
		p := nextRandom(seed) % (m * n)
		for isMark(grid[p/n][p%n]) {
			p = (p + 1) % (m * n)
		}
		grid[p/n][p%n] = mark
	}
	return grid
}

func main() {
	seed := int64(1263)
	grids := make([][][]byte, 100)
	for g := range grids {
		grids[g] = randomGrid(20, 20, 10, &seed)
	}
	buf := make([]state, ring)
	var check, total int64
	for round := int64(0); round < 20; round++ {
		for _, g := range grids {
			pushes := minPushBox(g, buf)
			if pushes > 0 {
				total += pushes
			}
			check = (check*131 + pushes + 1 + round) % 1000000007
		}
	}
	fmt.Printf("20 rounds of 100 grids of 20 by 20: %d pushes, checksum %d\n", total, check)
}
