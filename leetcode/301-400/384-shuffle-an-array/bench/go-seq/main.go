// Benchmark for #384: mirror of shuffle.kara (Fisher-Yates from the end).
package main

import "fmt"

type Solution struct {
	original []int64
	seed     int64
}

func (s *Solution) below(n int64) int64 {
	s.seed = (s.seed*1103515245 + 12345) % 2147483648
	return (s.seed / 65536) % n
}

func (s *Solution) shuffle() []int64 {
	a := make([]int64, len(s.original))
	copy(a, s.original)
	for i := int64(len(a)) - 1; i > 0; i-- {
		j := s.below(i + 1)
		a[i], a[j] = a[j], a[i]
	}
	return a
}

func main() {
	nums := make([]int64, 1000)
	for i := range nums {
		nums[i] = int64(i) * 7 % 1000
	}
	s := &Solution{nums, 384}
	var checksum int64
	for q := 0; q < 250000; q++ {
		a := s.shuffle()
		var sum int64
		for k := range a {
			sum += a[k] * int64(k+1)
		}
		checksum = (checksum*31 + sum) % 1000000007
	}
	fmt.Printf("250000 shuffles of 1000 values, checksum %d\n", checksum)
}
