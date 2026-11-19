// LeetCode #1642: Furthest Building You Can Reach -- the bench's Go
// mirror: the ★ arm on 50 random rows of 100000 buildings up to 10^4 high,
// each with up to 10^9 bricks and up to 5000 ladders, all drawn first.
package main

import (
	"container/heap"
	"fmt"
)

type minHeap []int32

func (h minHeap) Len() int           { return len(h) }
func (h minHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x any)        { *h = append(*h, x.(int32)) }
func (h *minHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func furthestBuilding(heights []int32, bricks, ladders int32) int64 {
	laddered := &minHeap{}
	for i := 1; i < len(heights); i++ {
		climb := heights[i] - heights[i-1]
		if climb <= 0 {
			continue
		}
		heap.Push(laddered, climb)
		if int32(laddered.Len()) > ladders {
			bricks -= heap.Pop(laddered).(int32)
			if bricks < 0 {
				return int64(i - 1)
			}
		}
	}
	return int64(len(heights) - 1)
}

var seed int64 = 1642

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type row struct {
		heights          []int32
		bricks, ladders int32
	}
	rows := make([]row, 50)
	for r := range rows {
		heights := make([]int32, 100000)
		for i := range heights {
			heights[i] = int32(nextRandom()%10000 + 1)
		}
		bricks := int32((nextRandom()*32768 + nextRandom()) % 1000000001)
		ladders := int32(nextRandom() % 5001)
		rows[r] = row{heights, bricks, ladders}
	}
	var check, total int64
	for _, r := range rows {
		furthest := furthestBuilding(r.heights, r.bricks, r.ladders)
		total += furthest
		check = (check*31 + furthest + 1) % 1000000007
	}
	fmt.Printf("50 rows of 100000 buildings: indices sum to %d, checksum %d\n", total, check)
}
