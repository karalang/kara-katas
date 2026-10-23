// LeetCode #911: Online Election -- bench program, Go.
//
// The leader after every vote, and a binary search for the time, on one
// election of 1,000,000 votes among 1,000 people, built once. Each query
// asks for the leader at a random time and folds the answer into a
// checksum; 2,000,000 queries.
package main

import "fmt"

type TopVotedCandidate struct {
	times   []int64
	leaders []int64
}

func newTopVotedCandidate(persons, times []int64) *TopVotedCandidate {
	n := len(persons)
	count := make([]int64, n)
	leaders := make([]int64, 0, n)
	leader := persons[0]
	for i := 0; i < n; i++ {
		p := persons[i]
		count[p]++
		if count[p] >= count[leader] {
			leader = p
		}
		leaders = append(leaders, leader)
	}
	return &TopVotedCandidate{times: append([]int64(nil), times...), leaders: leaders}
}

func (e *TopVotedCandidate) q(t int64) int64 {
	lo, hi := 0, len(e.times)
	for hi-lo > 1 {
		mid := (lo + hi) / 2
		if e.times[mid] <= t {
			lo = mid
		} else {
			hi = mid
		}
	}
	return e.leaders[lo]
}

var seed int64 = 911

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := 1000000
	queries := 2000000
	persons := make([]int64, 0, n)
	times := make([]int64, 0, n)
	var at int64
	for i := 0; i < n; i++ {
		persons = append(persons, nextRandom()%1000)
		times = append(times, at)
		at += 1 + nextRandom()%1000
	}
	e := newTopVotedCandidate(persons, times)
	var check int64
	for j := 0; j < queries; j++ {
		high := nextRandom()
		t := (high*32768 + nextRandom()) % at
		check = (check*31 + e.q(t)) % 1000000007
	}
	fmt.Printf("%d votes, %d queries: checksum %d\n", n, queries, check)
}
