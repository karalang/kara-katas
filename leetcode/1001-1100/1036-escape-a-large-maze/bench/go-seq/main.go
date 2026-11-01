// LeetCode #1036: Escape a Large Maze -- bench
// Mirrors ../escape_maze.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

type pt [2]int64

func notFenced(blocked map[pt]struct{}, from, to pt, side int64) bool {
	limit := len(blocked) * (len(blocked) - 1) / 2
	seen := map[pt]struct{}{from: {}}
	queue := []pt{from}
	for len(queue) > 0 {
		p := queue[0]
		queue = queue[1:]
		if p == to || len(seen) > limit {
			return true
		}
		for _, d := range [4]pt{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
			next := pt{p[0] + d[0], p[1] + d[1]}
			if next[0] >= 0 && next[0] < side && next[1] >= 0 && next[1] < side {
				if _, b := blocked[next]; !b {
					if _, s := seen[next]; !s {
						seen[next] = struct{}{}
						queue = append(queue, next)
					}
				}
			}
		}
	}
	return false
}

func isEscapePossible(blocked []pt, source, target pt) bool {
	walls := map[pt]struct{}{}
	for _, b := range blocked {
		walls[b] = struct{}{}
	}
	return notFenced(walls, source, target, 1000000) && notFenced(walls, target, source, 1000000)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rounds := 4
	seed := int64(1036)
	type maze struct {
		blocked        []pt
		source, target pt
	}
	mazes := []maze{}
	for k := 0; k < 30; k++ {
		blocked := []pt{}
		cx := nextRandom(&seed)%900000 + 50000
		cy := nextRandom(&seed)%900000 + 50000
		if k%3 == 2 {
			for i := int64(0); i < 200; i++ {
				blocked = append(blocked, pt{i, 199 - i})
			}
			mazes = append(mazes, maze{blocked, pt{200, 0}, pt{cx, cy}})
		} else {
			for i := int64(0); i < 50; i++ {
				blocked = append(blocked, pt{cx + i, cy + 50 - i}, pt{cx + 50 - i, cy - i}, pt{cx - i, cy - 50 + i}, pt{cx - 50 + i, cy + i})
			}
			if k%3 == 0 {
				mazes = append(mazes, maze{blocked, pt{cx + 10, cy - 10}, pt{0, 0}})
			} else {
				mazes = append(mazes, maze{blocked, pt{cx + 60, cy}, pt{999999, 999999}})
			}
		}
	}
	escapes := 0
	var check int64
	for r := 0; r < rounds; r++ {
		for _, m := range mazes {
			answer := isEscapePossible(m.blocked, m.source, m.target)
			v := int64(1)
			if answer {
				escapes++
				v = 2
			}
			check = (check*131 + v) % 1000000007
		}
	}
	fmt.Printf("30 mazes of 200 blocks, %d rounds: %d escapes, checksum %d\n", rounds, escapes, check)
}
