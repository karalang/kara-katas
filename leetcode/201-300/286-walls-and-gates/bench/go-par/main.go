// Goroutine mirror of wallsgates.kara's par lane — one goroutine per board,
// results collected through a channel and reduced in main. The per-board
// algorithm is identical to go-seq's.
package main

import (
	"fmt"
	"sync"
)

const inf int64 = 2147483647

func makeBoard(b, n int64) []int64 {
	g := make([]int64, 0, n)
	s := 777 + b*1013
	for i := int64(0); i < n; i++ {
		s = (s*1103515245 + 12345) % 2147483648
		roll := s % 100
		switch {
		case roll < 20:
			g = append(g, -1)
		case roll < 21:
			g = append(g, 0)
		default:
			g = append(g, inf)
		}
	}
	return g
}

func solve(template []int64, r, c int64) (int64, int64) {
	n := r * c
	g := make([]int64, n)
	copy(g, template)

	q := make([]int64, 0, n)
	for k := int64(0); k < n; k++ {
		if g[k] == 0 {
			q = append(q, k)
		}
	}

	for head := 0; head < len(q); head++ {
		cell := q[head]
		row, col := cell/c, cell%c
		d := g[cell] + 1
		if row > 0 {
			if nb := cell - c; g[nb] == inf {
				g[nb] = d
				q = append(q, nb)
			}
		}
		if row < r-1 {
			if nb := cell + c; g[nb] == inf {
				g[nb] = d
				q = append(q, nb)
			}
		}
		if col > 0 {
			if nb := cell - 1; g[nb] == inf {
				g[nb] = d
				q = append(q, nb)
			}
		}
		if col < c-1 {
			if nb := cell + 1; g[nb] == inf {
				g[nb] = d
				q = append(q, nb)
			}
		}
	}

	var total, unreachable int64
	for j := int64(0); j < n; j++ {
		if g[j] == inf {
			unreachable++
		} else if g[j] > 0 {
			total += g[j]
		}
	}
	return total, unreachable
}

func runBoard(b, r, c, reps int64) (int64, int64) {
	template := makeBoard(b, r*c)
	var total, unreachable int64
	for rep := int64(0); rep < reps; rep++ {
		t, u := solve(template, r, c)
		total += t
		unreachable += u
	}
	return total, unreachable
}

type boardResult struct{ total, unreachable int64 }

func main() {
	const boards, r, c, reps int64 = 16, 512, 512, 8
	parts := make([]boardResult, boards)
	var wg sync.WaitGroup
	for b := int64(0); b < boards; b++ {
		wg.Add(1)
		go func(b int64) {
			defer wg.Done()
			t, u := runBoard(b, r, c, reps)
			parts[b] = boardResult{t, u}
		}(b)
	}
	wg.Wait()

	var total, unreachable int64
	for _, p := range parts {
		total += p.total
		unreachable += p.unreachable
	}
	fmt.Printf("%d %d\n", total, unreachable)
}
