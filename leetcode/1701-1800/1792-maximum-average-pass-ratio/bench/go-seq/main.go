// LeetCode #1792: Maximum Average Pass Ratio -- the bench in Go: the ★ arm
// over 200 random lists of 1000 classes built once, 4000 calls. A max-heap
// of (gain, class) through container/heap, ties to the larger class.
package main

import (
	"container/heap"
	"fmt"
	"math"
)

type entry struct {
	g float64
	i int64
}

type queue []entry

func (q queue) Len() int { return len(q) }
func (q queue) Less(a, b int) bool {
	return q[a].g > q[b].g || (q[a].g == q[b].g && q[a].i > q[b].i)
}
func (q queue) Swap(a, b int)       { q[a], q[b] = q[b], q[a] }
func (q *queue) Push(x interface{}) { *q = append(*q, x.(entry)) }
func (q *queue) Pop() interface{} {
	old := *q
	e := old[len(old)-1]
	*q = old[:len(old)-1]
	return e
}

func gain(p, t int64) float64 {
	return float64(p+1)/float64(t+1) - float64(p)/float64(t)
}

func maxAverageRatio(classes [][]int32, extraStudents int32) float64 {
	n := len(classes)
	pass := make([]int64, n)
	total := make([]int64, n)
	for i, c := range classes {
		pass[i] = int64(c[0])
		total[i] = int64(c[1])
	}
	q := &queue{}
	for i := 0; i < n; i++ {
		heap.Push(q, entry{gain(pass[i], total[i]), int64(i)})
	}
	for s := int32(0); s < extraStudents; s++ {
		i := heap.Pop(q).(entry).i
		pass[i]++
		total[i]++
		heap.Push(q, entry{gain(pass[i], total[i]), i})
	}
	sum := 0.0
	for i := 0; i < n; i++ {
		sum += float64(pass[i]) / float64(total[i])
	}
	return sum / float64(n)
}

var seed int64 = 1792

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][][]int32, 0, 200)
	for l := 0; l < 200; l++ {
		classes := make([][]int32, 0, 1000)
		for c := 0; c < 1000; c++ {
			t := 1 + nextRandom()%1000
			p := 1 + nextRandom()%t
			classes = append(classes, []int32{int32(p), int32(t)})
		}
		lists = append(lists, classes)
	}
	var check int64
	for call := int64(0); call < 4000; call++ {
		classes := lists[(check+call)%200]
		extra := 1 + check%1000
		r := maxAverageRatio(classes, int32(extra))
		check = (check*31 + int64(math.Floor(r*100000.0+0.5))) % 1000000007
	}
	fmt.Printf("4000 calls over 200 lists of 1000 classes: checksum %d\n", check)
}
