// LeetCode #2386: Find the K-Sum of an Array -- the bench, the ★ arm in
// Go: the largest sum less the (k-1)-th smallest nonempty sum of the
// sorted sizes, walked from the smallest by a heap of (sum, last place).
package main

import (
	"container/heap"
	"fmt"
	"sort"
)

type entry struct{ sum, last int64 }

type queue []entry

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	return q[i].sum < q[j].sum || (q[i].sum == q[j].sum && q[i].last < q[j].last)
}
func (q queue) Swap(i, j int)       { q[i], q[j] = q[j], q[i] }
func (q *queue) Push(x interface{}) { *q = append(*q, x.(entry)) }
func (q *queue) Pop() interface{} {
	old := *q
	e := old[len(old)-1]
	*q = old[:len(old)-1]
	return e
}

func kSum(nums []int64, k int64) int64 {
	largest := int64(0)
	sizes := make([]int64, len(nums))
	for i, v := range nums {
		if v > 0 {
			largest += v
		}
		if v < 0 {
			v = -v
		}
		sizes[i] = v
	}
	sort.Slice(sizes, func(i, j int) bool { return sizes[i] < sizes[j] })
	q := &queue{{sizes[0], 0}}
	lost := int64(0)
	for step := int64(1); step < k; step++ {
		e := heap.Pop(q).(entry)
		lost = e.sum
		if e.last+1 < int64(len(sizes)) {
			heap.Push(q, entry{e.sum + sizes[e.last+1], e.last + 1})
			heap.Push(q, entry{e.sum - sizes[e.last] + sizes[e.last+1], e.last + 1})
		}
	}
	return largest - lost
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	high := nextRandom(seed)
	return high*32768 + nextRandom(seed)
}

func main() {
	// 10 arrays of 10^5 values from -10^9 to 10^9; pass p asks array a for
	// k = 2000 - (7 p + a) % 100
	seed := int64(2386)
	arrays := make([][]int64, 10)
	for a := range arrays {
		arrays[a] = make([]int64, 100000)
		for i := range arrays[a] {
			arrays[a][i] = wide(&seed)%2000000001 - 1000000000
		}
	}
	check := int64(0)
	for p := int64(0); p < 60; p++ {
		for a := int64(0); a < 10; a++ {
			answer := kSum(arrays[a], 2000-(7*p+a)%100)
			check = (check*31 + answer%1000000007 + 1000000007 + p) % 1000000007
		}
	}
	fmt.Printf("60 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
