// Benchmark for #519: Go mirror of the ★ arm (a shuffle kept in a map);
// see ../random_flip_matrix.kara. A built-in map, a fresh one for every
// grid, as the ★ arm's `Map.new()`.
package main

import "fmt"

type Draw struct {
	seed int64
}

func (d *Draw) step() int64 {
	d.seed = (d.seed*1103515245 + 12345) % 2147483648
	return d.seed / 65536
}

// Uniform in [0, n) for n up to 2^30: 30 random bits, drawn again when
// they land in the last, incomplete run of n.
func (d *Draw) below(n int64) int64 {
	limit := 1073741824 / n * n
	for {
		high := d.step()
		low := d.step()
		r := high*32768 + low
		if r < limit {
			return r % n
		}
	}
}

type Solution struct {
	m, n, free int64
	moved      map[int64]int64
	draw       Draw
}

func newSolution(m, n, seed int64) *Solution {
	return &Solution{m: m, n: n, free: m * n, moved: map[int64]int64{}, draw: Draw{seed}}
}

// What slot i of the shuffled cells holds.
func (s *Solution) at(i int64) int64 {
	if cell, ok := s.moved[i]; ok {
		return cell
	}
	return i
}

func (s *Solution) flip() []int64 {
	r := s.draw.below(s.free)
	s.free--
	cell := s.at(r)
	last := s.at(s.free)
	s.moved[r] = last
	return []int64{cell / s.n, cell % s.n}
}

func (s *Solution) reset() {
	clear(s.moved)
	s.free = s.m * s.n
}

var seed int64 = 519

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 10,000 grids of up to 10,000 by 10,000, 1,000 calls on each: a
	// reset one time in a hundred and whenever the grid is full, else a
	// flip.
	var checksum int64
	grids := int64(10000)
	for g := int64(0); g < grids; g++ {
		high := nextRandom()
		m := 1 + (high*32768+nextRandom())%10000
		high = nextRandom()
		n := 1 + (high*32768+nextRandom())%10000
		solution := newSolution(m, n, g)
		free := m * n
		for i := 0; i < 1000; i++ {
			if free == 0 || nextRandom()%100 == 0 {
				solution.reset()
				free = m * n
			} else {
				p := solution.flip()
				free--
				checksum = (checksum*31 + p[0]*10000 + p[1]) % 1000000007
			}
		}
	}
	fmt.Printf("%d grids, 1000 calls each: checksum %d\n", grids, checksum)
}
