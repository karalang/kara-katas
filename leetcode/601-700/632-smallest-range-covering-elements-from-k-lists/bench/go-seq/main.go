// LeetCode 632 -- Smallest Range Covering Elements from K Lists, bench
// mirror in Go.
//
// The ★ arm of smallest_range.kara: one value from each list in a
// smallest-first `container/heap` of (value, list, index) triples, with
// the largest held value tracked beside it. Same 10 inputs, same 30
// rounds, same output line.
package main

import (
	"container/heap"
	"fmt"
	"sort"
)

type entry struct{ value, list, at int64 }

type queue []entry

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	if q[i].value != q[j].value {
		return q[i].value < q[j].value
	}
	if q[i].list != q[j].list {
		return q[i].list < q[j].list
	}
	return q[i].at < q[j].at
}
func (q queue) Swap(i, j int)       { q[i], q[j] = q[j], q[i] }
func (q *queue) Push(x interface{}) { *q = append(*q, x.(entry)) }
func (q *queue) Pop() interface{} {
	old := *q
	e := old[len(old)-1]
	*q = old[:len(old)-1]
	return e
}

func smallestRange(nums [][]int64) []int64 {
	q := &queue{}
	high := nums[0][0]
	for list := range nums {
		heap.Push(q, entry{nums[list][0], int64(list), 0})
		high = max(high, nums[list][0])
	}
	var bestLow, bestHigh int64
	found := false
	for {
		e := heap.Pop(q).(entry)
		if !found || high-e.value < bestHigh-bestLow {
			bestLow, bestHigh, found = e.value, high, true
		}
		if e.at+1 == int64(len(nums[e.list])) {
			break
		}
		next := nums[e.list][e.at+1]
		high = max(high, next)
		heap.Push(q, entry{next, e.list, e.at + 1})
	}
	return []int64{bestLow, bestHigh}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomLists(count, length int, seed *int64) [][]int64 {
	nums := [][]int64{}
	for i := 0; i < count; i++ {
		list := []int64{}
		for j := 0; j < length; j++ {
			wide := nextRandom(seed) * 32768
			wide += nextRandom(seed)
			list = append(list, wide%200001-100000)
		}
		sort.Slice(list, func(a, b int) bool { return list[a] < list[b] })
		nums = append(nums, list)
	}
	return nums
}

func main() {
	seed := int64(632)
	inputs := [][][]int64{}
	for i := 0; i < 10; i++ {
		inputs = append(inputs, randomLists(3500, 50, &seed))
	}
	rounds := 30
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		r := smallestRange(inputs[round%10])
		total += r[1] - r[0]
		checksum = (checksum*31 + r[0]*101 + r[1] + 100000000) % 1000000007
	}
	fmt.Printf("10 inputs of 3500 lists, %d rounds: total width %d, checksum %d\n", rounds, total, checksum)
}
