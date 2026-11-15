// LeetCode #1157 bench: the ★ arm's vote tree and sorted places, the same
// workload as majority_checker.kara.
package main

import (
	"fmt"
	"sort"
)

type pair struct{ value, votes int64 }

func vote(a, b pair) pair {
	if a.value == b.value {
		return pair{a.value, a.votes + b.votes}
	}
	if a.votes >= b.votes {
		return pair{a.value, a.votes - b.votes}
	}
	return pair{b.value, b.votes - a.votes}
}

type checker struct {
	size   int64
	tree   []pair
	places [][]int64
}

func newChecker(arr []int32) *checker {
	n := int64(len(arr))
	size := int64(1)
	for size < n {
		size *= 2
	}
	tree := make([]pair, 2*size)
	places := make([][]int64, 20001)
	for i, x := range arr {
		tree[size+int64(i)] = pair{int64(x), 1}
		places[x] = append(places[x], int64(i))
	}
	for i := size - 1; i >= 1; i-- {
		tree[i] = vote(tree[2*i], tree[2*i+1])
	}
	return &checker{size, tree, places}
}

func (c *checker) query(left, right, threshold int64) int64 {
	lo, hi := left+c.size, right+c.size+1
	won := pair{0, 0}
	for lo < hi {
		if lo%2 == 1 {
			won = vote(won, c.tree[lo])
			lo++
		}
		if hi%2 == 1 {
			hi--
			won = vote(won, c.tree[hi])
		}
		lo /= 2
		hi /= 2
	}
	p := c.places[won.value]
	count := int64(sort.Search(len(p), func(i int) bool { return p[i] > right }) - sort.Search(len(p), func(i int) bool { return p[i] >= left }))
	if count >= threshold {
		return won.value
	}
	return -1
}

var seed int64 = 1157

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const passes = 100
	var checkers []*checker
	var queries [][][3]int64
	for kind := 0; kind < 4; kind++ {
		v := 1 + nextRandom()%20000
		arr := make([]int32, 20000)
		for i := range arr {
			var x int64
			limit := int64(50)
			if kind == 1 {
				limit = 67
			}
			if kind == 0 {
				x = 1 + nextRandom()%2
			} else if kind == 2 {
				x = 1 + nextRandom()%20000
			} else if nextRandom()%100 < limit {
				x = v
			} else {
				x = 1 + nextRandom()%20000
			}
			arr[i] = int32(x)
		}
		checkers = append(checkers, newChecker(arr))
		qs := make([][3]int64, 10000)
		for q := range qs {
			a, b := nextRandom()%20000, nextRandom()%20000
			left, right := min(a, b), max(a, b)
			least := (right-left+1)/2 + 1
			qs[q] = [3]int64{left, right, least + nextRandom()%(right-left+2-least)}
		}
		queries = append(queries, qs)
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for k := 0; k < 4; k++ {
			for _, q := range queries[k] {
				check = (check*31 + checkers[k].query(q[0], q[1], q[2]) + p + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d passes over 4 arrays of 20000 values, 10000 queries each: checksum %d\n", passes, check)
}
