// LeetCode #2102: Sequentially Ordinal Rank Tracker -- Go mirror of the ★
// arm's benchmark (rank_tracker.kara): the same 20 runs of 4 * 10^4
// calls, two container/heap heaps of places, the served one worst on top
// and the waiting one best on top.
package main

import (
	"container/heap"
	"fmt"
)

type place struct {
	score int64
	name  string
}

// better: a higher score, then the smaller name
func better(a, b place) bool {
	if a.score != b.score {
		return a.score > b.score
	}
	return a.name < b.name
}

type worstFirst []place

func (h worstFirst) Len() int            { return len(h) }
func (h worstFirst) Less(i, j int) bool  { return better(h[j], h[i]) }
func (h worstFirst) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *worstFirst) Push(x interface{}) { *h = append(*h, x.(place)) }
func (h *worstFirst) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type bestFirst []place

func (h bestFirst) Len() int            { return len(h) }
func (h bestFirst) Less(i, j int) bool  { return better(h[i], h[j]) }
func (h bestFirst) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *bestFirst) Push(x interface{}) { *h = append(*h, x.(place)) }
func (h *bestFirst) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type tracker struct {
	served  worstFirst
	waiting bestFirst
}

func (t *tracker) add(name string, score int64) {
	heap.Push(&t.served, place{score, name})
	heap.Push(&t.waiting, heap.Pop(&t.served).(place))
}

func (t *tracker) get() string {
	best := heap.Pop(&t.waiting).(place)
	heap.Push(&t.served, best)
	return best.name
}

var seed int64 = 2102

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	gets := 0
	var check int64
	for r := 0; r < 20; r++ {
		taken := map[string]bool{}
		t := &tracker{}
		added, asked := 0, 0
		for asked < 20000 {
			if added < 20000 && (asked == added || nextRandom()%2 == 0) {
				var name string
				for {
					n := nextRandom()%10 + 1
					b := make([]byte, n)
					for i := range b {
						b[i] = byte('a' + nextRandom()%26)
					}
					name = string(b)
					if !taken[name] {
						taken[name] = true
						break
					}
				}
				t.add(name, wideRandom()%100000+1)
				added++
			} else {
				name := t.get()
				asked++
				gets++
				for i := 0; i < len(name); i++ {
					check = (check*31 + int64(name[i])) % 1000000007
				}
				check = (check*31 + 7) % 1000000007
			}
		}
	}
	fmt.Printf("20 runs: %d gets, checksum %d\n", gets, check)
}
