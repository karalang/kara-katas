// Benchmark for #528: Go mirror of the ★ arm (prefix sums and a binary
// search); see ../random_pick_with_weight.kara. The same seeded
// generator, so the same picks.
package main

import "fmt"

type Draw struct{ seed int64 }

func (d *Draw) step() int64 {
	d.seed = (d.seed*1103515245 + 12345) % 2147483648
	return d.seed / 65536
}

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
	ends []int64
	draw Draw
}

func newSolution(w []int64, seed int64) *Solution {
	ends := []int64{}
	total := int64(0)
	for _, x := range w {
		total += x
		ends = append(ends, total)
	}
	return &Solution{ends, Draw{seed}}
}

func (s *Solution) pickIndex() int64 {
	r := s.draw.below(s.ends[len(s.ends)-1])
	low, high := 0, len(s.ends)-1
	for low < high {
		mid := (low + high) / 2
		if s.ends[mid] > r {
			high = mid
		} else {
			low = mid + 1
		}
	}
	return int64(low)
}

func main() {
	seed := int64(528)
	lists := [][]int64{}
	for l := 0; l < 20; l++ {
		w := []int64{}
		for i := 0; i < 10000; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			high := seed / 65536
			seed = (seed*1103515245 + 12345) % 2147483648
			w = append(w, 1+(high*32768+seed/65536)%100000)
		}
		lists = append(lists, w)
	}
	total, checksum := int64(0), int64(0)
	for round := int64(0); round < 50; round++ {
		for l := range lists {
			s := newSolution(lists[l], round*20+int64(l))
			for k := 0; k < 10000; k++ {
				i := s.pickIndex()
				total += i
				checksum = (checksum*31 + i) % 1000000007
			}
		}
	}
	fmt.Printf("20 lists of 10000, 50 rounds of 10000 picks: total %d, checksum %d\n", total, checksum)
}
