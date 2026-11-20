// LeetCode #1705: Maximum Number of Eaten Apples -- the bench's Go
// mirror: the ★ arm on 50 random trees of 20000 days, all drawn first,
// each answered 10 times.
package main

import (
	"container/heap"
	"fmt"
)

type crop struct {
	rot  int64
	left int32
}

// a min-heap of crops, by (rotting day, apples left)
type crops []crop

func (h crops) Len() int { return len(h) }
func (h crops) Less(i, j int) bool {
	return h[i].rot < h[j].rot || (h[i].rot == h[j].rot && h[i].left < h[j].left)
}
func (h crops) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *crops) Push(x any)   { *h = append(*h, x.(crop)) }
func (h *crops) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

// each day the rotten crops dropped and one apple eaten from the soonest to rot
func eatenApples(apples, days []int32) int32 {
	n := int64(len(apples))
	queue := &crops{}
	var eaten int32
	for day := int64(0); day < n || queue.Len() > 0; day++ {
		if day < n && apples[day] > 0 {
			heap.Push(queue, crop{day + int64(days[day]), apples[day]})
		}
		for queue.Len() > 0 && (*queue)[0].rot <= day {
			heap.Pop(queue)
		}
		if queue.Len() > 0 {
			c := heap.Pop(queue).(crop)
			eaten++
			if c.left > 1 {
				heap.Push(queue, crop{c.rot, c.left - 1})
			}
		}
	}
	return eaten
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1705

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50, 10, 20000
	allApples := make([][]int32, count)
	allDays := make([][]int32, count)
	for c := 0; c < count; c++ {
		apples := make([]int32, 0, n)
		days := make([]int32, 0, n)
		for i := 0; i < n; i++ {
			// one day in four grows nothing
			var grown int64
			if nextRandom()%4 != 0 {
				grown = nextRandom()%20000 + 1
			}
			apples = append(apples, int32(grown))
			if grown == 0 {
				days = append(days, 0)
			} else {
				days = append(days, int32(nextRandom()%20000+1))
			}
		}
		allApples[c] = apples
		allDays[c] = days
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			answer := int64(eatenApples(allApples[c], allDays[c]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d trees of %d days, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
