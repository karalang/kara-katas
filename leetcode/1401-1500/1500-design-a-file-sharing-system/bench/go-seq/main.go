// LeetCode #1500: Design a File Sharing System -- the benchmark, the same
// structure as files.kara: each chunk's owners in a sorted slice kept by
// binary search, each user's chunks in a slice indexed by id, free ids in a
// min-heap.
package main

import (
	"container/heap"
	"fmt"
)

type minHeap []int64

func (h minHeap) Len() int            { return len(h) }
func (h minHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(int64)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type FileSharing struct {
	owners [][]int64
	owned  [][]int64
	free   *minHeap
}

func position(v []int64, x int64) int {
	lo, hi := 0, len(v)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if v[mid] < x {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func insertAt(v []int64, at int, x int64) []int64 {
	v = append(v, 0)
	copy(v[at+1:], v[at:])
	v[at] = x
	return v
}

func NewFileSharing(m int64) *FileSharing {
	return &FileSharing{owners: make([][]int64, m+1), owned: [][]int64{nil}, free: &minHeap{}}
}

func (f *FileSharing) Join(chunks []int64) int64 {
	var id int64
	if f.free.Len() > 0 {
		id = heap.Pop(f.free).(int64)
	} else {
		f.owned = append(f.owned, nil)
		id = int64(len(f.owned) - 1)
	}
	for _, c := range chunks {
		f.owners[c] = insertAt(f.owners[c], position(f.owners[c], id), id)
	}
	f.owned[id] = chunks
	return id
}

func (f *FileSharing) Leave(id int64) {
	for _, c := range f.owned[id] {
		o := f.owners[c]
		at := position(o, id)
		f.owners[c] = append(o[:at], o[at+1:]...)
	}
	f.owned[id] = nil
	heap.Push(f.free, id)
}

func (f *FileSharing) Request(id, chunk int64) []int64 {
	o := f.owners[chunk]
	answer := make([]int64, len(o))
	copy(answer, o)
	if len(answer) > 0 {
		at := position(o, id)
		if at == len(o) || o[at] != id {
			f.owners[chunk] = insertAt(o, at, id)
			f.owned[id] = append(f.owned[id], chunk)
		}
	}
	return answer
}

var seed int64 = 1500

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func randomChunks(m, most int64) []int64 {
	if most > m {
		most = m
	}
	count := nextRandom() % (most + 1)
	chunks := []int64{}
	for int64(len(chunks)) < count {
		c := nextRandom()%m + 1
		seen := false
		for _, x := range chunks {
			if x == c {
				seen = true
			}
		}
		if !seen {
			chunks = append(chunks, c)
		}
	}
	return chunks
}

func simulate(m, ops, most int64) (int64, int64, int64, int64) {
	system := NewFileSharing(m)
	live := []int64{}
	var joins, requests, owners, check int64
	for k := int64(0); k < ops; k++ {
		r := nextRandom() % 10
		if len(live) == 0 || r < 3 {
			id := system.Join(randomChunks(m, most))
			live = append(live, id)
			joins++
			check = mix(check, id)
		} else if r < 5 {
			at := nextRandom() % int64(len(live))
			id := live[at]
			live[at] = live[len(live)-1]
			live = live[:len(live)-1]
			system.Leave(id)
		} else {
			user := live[nextRandom()%int64(len(live))]
			chunk := nextRandom()%m + 1
			answer := system.Request(user, chunk)
			requests++
			owners += int64(len(answer))
			check = mix(check, int64(len(answer)))
			for _, x := range answer {
				check = mix(check, x)
			}
		}
	}
	return joins, requests, owners, check
}

func batch(count, mostM, ops, most int64) {
	var joins, requests, owners, check int64
	for i := int64(0); i < count; i++ {
		m := nextRandom()%mostM + 1
		j, r, o, c := simulate(m, ops, most)
		joins += j
		requests += r
		owners += o
		check = mix(check, c)
	}
	fmt.Printf("%d systems of up to %d chunks, %d calls each: %d joins, %d requests, %d owners returned, checksum %d\n",
		count, mostM, ops, joins, requests, owners, check)
}

func main() {
	batch(40, 2000, 40000, 30)
}
