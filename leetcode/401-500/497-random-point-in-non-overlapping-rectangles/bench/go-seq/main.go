// Benchmark for #497: Go mirror of the ★ arm (prefix sums); see
// ../random_point_rects.kara.
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
	rects [][]int64
	ends  []int64
	draw  Draw
}

func newSolution(rects [][]int64, seed int64) *Solution {
	ends := []int64{}
	var total int64
	for _, r := range rects {
		total += (r[2] - r[0] + 1) * (r[3] - r[1] + 1)
		ends = append(ends, total)
	}
	return &Solution{rects: rects, ends: ends, draw: Draw{seed}}
}

func (s *Solution) pick() []int64 {
	k := s.draw.below(s.ends[len(s.ends)-1])
	low, high := 0, len(s.ends)-1
	for low < high {
		mid := (low + high) / 2
		if s.ends[mid] > k {
			high = mid
		} else {
			low = mid + 1
		}
	}
	r := s.rects[low]
	var before int64
	if low > 0 {
		before = s.ends[low-1]
	}
	at := k - before
	width := r[2] - r[0] + 1
	return []int64{r[0] + at%width, r[1] + at/width}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 500 sets of 100 rectangles (the problem's most) of 1 to 2,001 on a
	// side, spread across the whole range, built once. Then each set gets
	// a fresh solution and 10,000 picks (the problem's most).
	sets := 500
	var seed int64 = 497
	all := [][][]int64{}
	for c := 0; c < sets; c++ {
		rects := [][]int64{}
		for i := int64(0); i < 100; i++ {
			x := -1000000000 + i*19000000 + nextRandom(&seed)%1000
			y := nextRandom(&seed)%30000*60000 - 999000000
			w := 1 + nextRandom(&seed)%2001
			h := 1 + nextRandom(&seed)%2001
			rects = append(rects, []int64{x, y, x + w - 1, y + h - 1})
		}
		all = append(all, rects)
	}
	var sum, checksum int64
	for k := 0; k < sets; k++ {
		rects := make([][]int64, len(all[k]))
		for i, r := range all[k] {
			rects[i] = append([]int64{}, r...)
		}
		solution := newSolution(rects, int64(k))
		for j := 0; j < 10000; j++ {
			// Moved up by 10^9 so that every coordinate is at least 0.
			p := solution.pick()
			x := p[0] + 1000000000
			y := p[1] + 1000000000
			sum += x%1000 + y%1000
			checksum = (checksum*31 + x + 2*y) % 1000000007
		}
	}
	fmt.Printf("%d sets of 100, 10000 picks each: sum of last three digits %d, checksum %d\n", sets, sum, checksum)
}
