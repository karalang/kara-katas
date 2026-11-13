// LeetCode #1146: Snapshot Array -- the Go mirror of the ★ arm: a history
// of (snap, value) pairs for each place, the last pair at or before the
// snap asked found with sort.Search (`partition_point`).
package main

import (
	"fmt"
	"sort"
)

type pair struct{ snap, val int64 }

type SnapshotArray struct {
	history [][]pair
	snaps   int64
}

func newSnapshotArray(length int) *SnapshotArray {
	h := make([][]pair, length)
	for i := range h {
		h[i] = []pair{{0, 0}}
	}
	return &SnapshotArray{history: h}
}

func (a *SnapshotArray) Set(index int, val int64) {
	h := a.history[index]
	last := len(h) - 1
	if h[last].snap == a.snaps {
		h[last].val = val
	} else {
		a.history[index] = append(h, pair{a.snaps, val})
	}
}

func (a *SnapshotArray) Snap() int64 {
	a.snaps++
	return a.snaps - 1
}

func (a *SnapshotArray) Get(index int, snapID int64) int64 {
	h := a.history[index]
	return h[sort.Search(len(h), func(k int) bool { return h[k].snap > snapID })-1].val
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	a := nextRandom(seed)
	return a*32768 + nextRandom(seed)
}

func main() {
	n := int64(50000)
	arr := newSnapshotArray(int(n))
	seed := int64(1146)
	var total, check int64
	for r := int64(0); r < 50000; r++ {
		for k := 0; k < 50; k++ {
			i := wide(&seed) % n
			v := wide(&seed) % 1000000001
			arr.Set(int(i), v)
		}
		arr.Snap()
		for k := 0; k < 50; k++ {
			i := wide(&seed) % n
			s := wide(&seed) % (r + 1)
			got := arr.Get(int(i), s)
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("50000 rounds of 50 sets, a snap and 50 gets on 50000 places: gets total %d, checksum %d\n", total, check)
}
