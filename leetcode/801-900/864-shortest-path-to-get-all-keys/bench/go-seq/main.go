// LeetCode #864: Shortest Path to Get All Keys -- Go mirror of the bench
// program (the ★ arm, breadth-first search over (cell, keys held) states).
// The queue is a slice with a moving head.
package main

import (
	"fmt"
	"strings"
)

type state struct {
	cell, held, steps int64
}

func shortestPathAllKeys(grid []string) int64 {
	rows := int64(len(grid))
	cols := int64(len(grid[0]))
	cells := []byte(strings.Join(grid, ""))
	size := int64(len(cells))
	var start, keys int64
	for i := int64(0); i < size; i++ {
		if cells[i] == '@' {
			start = i
		} else if cells[i] >= 'a' && cells[i] <= 'f' {
			keys++
		}
	}
	all := int64(1)<<keys - 1
	seen := make([]bool, size<<keys)
	queue := []state{{start, 0, 0}}
	seen[start] = true
	dr := [4]int64{-1, 1, 0, 0}
	dc := [4]int64{0, 0, -1, 1}
	for head := 0; head < len(queue); head++ {
		s := queue[head]
		if s.held == all {
			return s.steps
		}
		r, c := s.cell/cols, s.cell%cols
		for d := 0; d < 4; d++ {
			nr, nc := r+dr[d], c+dc[d]
			if nr < 0 || nr >= rows || nc < 0 || nc >= cols {
				continue
			}
			next := nr*cols + nc
			b := cells[next]
			if b == '#' {
				continue
			}
			if b >= 'A' && b <= 'F' && s.held&(1<<(b-'A')) == 0 {
				continue
			}
			now := s.held
			if b >= 'a' && b <= 'f' {
				now = s.held | 1<<(b-'a')
			}
			if !seen[now*size+next] {
				seen[now*size+next] = true
				queue = append(queue, state{next, now, s.steps + 1})
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
	rows, cols, rounds := int64(30), int64(30), 1000
	seed := int64(864)
	cells := make([]byte, rows*cols)
	for i := range cells {
		if nextRandom(&seed)%100 < 20 {
			cells[i] = '#'
		} else {
			cells[i] = '.'
		}
	}
	for i := 0; i < 12; i++ {
		at := nextRandom(&seed) % (rows * cols)
		for cells[at] != '.' {
			at = nextRandom(&seed) % (rows * cols)
		}
		if i < 6 {
			cells[at] = byte('a' + i)
		} else {
			cells[at] = byte('A' + i - 6)
		}
	}
	var reached, total, check int64
	for k := 0; k < rounds; k++ {
		start := nextRandom(&seed) % (rows * cols)
		for cells[start] != '.' {
			start = nextRandom(&seed) % (rows * cols)
		}
		cells[start] = '@'
		grid := make([]string, rows)
		for r := int64(0); r < rows; r++ {
			grid[r] = string(cells[r*cols : (r+1)*cols])
		}
		cells[start] = '.'
		moves := shortestPathAllKeys(grid)
		if moves >= 0 {
			reached++
			total += moves
		}
		check = (check*31 + moves + 2) % 1000000007
	}
	fmt.Printf("%d starts on a 30 by 30 grid: %d reach every key, moves sum to %d, checksum %d\n", rounds, reached, total, check)
}
