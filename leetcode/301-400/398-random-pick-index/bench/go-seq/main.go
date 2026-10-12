// Benchmark for #398: mirror of random_pick_index.kara (reservoir sampling).
package main

import "fmt"

type Solution struct {
	nums []int64
	seed int64
}

func (s *Solution) below(n int64) int64 {
	s.seed = (s.seed*1103515245 + 12345) % 2147483648
	return (s.seed / 65536) % n
}

func (s *Solution) pick(target int64) int64 {
	kept := int64(-1)
	var seen int64
	for i := range s.nums {
		if s.nums[i] == target {
			seen++
			if s.below(seen) == 0 {
				kept = int64(i)
			}
		}
	}
	return kept
}

func main() {
	picks := int64(10000)
	seed := int64(3980)
	nums := make([]int64, 20000)
	for i := range nums {
		seed = (seed*1103515245 + 12345) % 2147483648
		nums[i] = (seed / 65536) % 10
	}
	s := &Solution{nums, 398}
	var total, checksum int64
	for p := int64(0); p < picks; p++ {
		r := s.pick(p % 10)
		total += r
		checksum = (checksum*31 + r) % 1000000007
	}
	fmt.Printf("%d picks: total %d, checksum %d\n", picks, total, checksum)
}
