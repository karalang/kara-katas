// LeetCode #1756: Design Most Recently Used Queue -- the bench (mru.kara
// in Go): a slice.
package main

import "fmt"

type MruQueue struct {
	values []int32
}

func newMruQueue(n int32) *MruQueue {
	q := &MruQueue{values: make([]int32, n)}
	for i := range q.values {
		q.values[i] = int32(i) + 1
	}
	return q
}

func (q *MruQueue) fetch(k int32) int32 {
	value := q.values[k-1]
	copy(q.values[k-1:], q.values[k:])
	q.values[len(q.values)-1] = value
	return value
}

var seed int64 = 1756

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, calls = 10000, 2000, 2000
	fetches := make([]int32, calls)
	for i := range fetches {
		fetches[i] = int32(nextRandom()%n + 1)
	}
	var sum, check int64
	for r := int64(0); r < count; r++ {
		queue := newMruQueue(n)
		for _, k := range fetches {
			got := int64(queue.fetch(k))
			sum += got
			check = (check*31 + got + r) % 1000000007
		}
	}
	fmt.Printf("%d queues of %d values, %d fetches each: fetched values add to %d, checksum %d\n", count, n, calls, sum, check)
}
