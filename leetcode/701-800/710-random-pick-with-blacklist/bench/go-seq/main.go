// LeetCode #710: Random Pick with Blacklist -- the r-th allowed number,
// by binary search.
// Benchmark mirror of the Kara rank arm: sort the blacklist; the r-th
// allowed number is r + i, i the first index with more than r allowed
// numbers below its blacklisted number.
package main

import (
	"fmt"
	"slices"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomBelow(seed *int64, bound int64) int64 {
	hi := nextRandom(seed)
	lo := nextRandom(seed)
	return (hi*32768 + lo) % bound
}

type Solution struct {
	bound int64
	black []int64
	seed  int64
}

func newSolution(n int64, blacklist []int64, seed int64) *Solution {
	black := slices.Clone(blacklist)
	slices.Sort(black)
	return &Solution{bound: n - int64(len(black)), black: black, seed: seed}
}

func (s *Solution) pickFrom(r int64) int64 {
	lo, hi := 0, len(s.black)
	for lo < hi {
		mid := (lo + hi) / 2
		if s.black[mid]-int64(mid) > r {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return r + int64(lo)
}

func (s *Solution) pick() int64 {
	r := randomBelow(&s.seed, s.bound)
	return s.pickFrom(r)
}

func main() {
	n := int64(1000000000)
	seed := int64(710)
	blacklist := make([]int64, 0, 100000)
	for i := int64(0); i < 100000; i++ {
		blacklist = append(blacklist, i*10000+randomBelow(&seed, 10000))
	}
	for i := int64(99999); i > 0; i-- {
		j := randomBelow(&seed, i+1)
		blacklist[i], blacklist[j] = blacklist[j], blacklist[i]
	}
	sum := int64(0)
	for round := int64(0); round < 5; round++ {
		s := newSolution(n, blacklist, 1+round)
		for k := 0; k < 1000000; k++ {
			sum += s.pick()
		}
	}
	fmt.Printf("5 rounds of 1000000 picks, 100000 of 1000000000 blacklisted: sum %d\n", sum)
}
