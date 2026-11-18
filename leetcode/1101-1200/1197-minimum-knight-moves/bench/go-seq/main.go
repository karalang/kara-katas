// LeetCode #1197 bench: the ★ arm in Go, over the same 2000 random targets
// as the Kāra bench; the queue is a slice used as a FIFO with a head index.
package main

import "fmt"

var moves = [8][2]int64{{1, 2}, {2, 1}, {2, -1}, {1, -2}, {-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}}

func abs(v int64) int64 {
	if v < 0 {
		return -v
	}
	return v
}

func minKnightMoves(x, y int64) int64 {
	tx, ty := abs(x), abs(y)
	const side = 305
	seen := make([]bool, side*side)
	queue := [][3]int64{{0, 0, 0}}
	seen[2*side+2] = true
	for head := 0; head < len(queue); head++ {
		cx, cy, steps := queue[head][0], queue[head][1], queue[head][2]
		if cx == tx && cy == ty {
			return steps
		}
		for _, m := range moves {
			nx, ny := cx+m[0], cy+m[1]
			if nx >= -2 && ny >= -2 && nx <= 302 && ny <= 302 {
				k := (nx+2)*side + ny + 2
				if !seen[k] {
					seen[k] = true
					queue = append(queue, [3]int64{nx, ny, steps + 1})
				}
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
	seed := int64(1197)
	targets := make([][2]int64, 0, 2000)
	for i := 0; i < 2000; i++ {
		s := nextRandom(&seed) % 301
		x := nextRandom(&seed) % (s + 1)
		y := s - x
		if nextRandom(&seed)%2 != 0 {
			x = -x
		}
		if nextRandom(&seed)%2 != 0 {
			y = -y
		}
		targets = append(targets, [2]int64{x, y})
	}
	var check int64
	for _, t := range targets {
		m := minKnightMoves(t[0], t[1])
		check = (check*131 + m + 1) % 1000000007
	}
	fmt.Printf("2000 targets: checksum %d\n", check)
}
