// LeetCode #622: Design Circular Queue -- Go mirror of the Kāra bench.
//
// The ★ arm's ring with a start and a count, on the same script and
// queues.
package main

import "fmt"

type MyCircularQueue struct {
	data  []int64
	head  int64
	count int64
}

func newQueue(k int64) *MyCircularQueue {
	return &MyCircularQueue{data: make([]int64, k)}
}

func (q *MyCircularQueue) EnQueue(value int64) bool {
	if q.count == int64(len(q.data)) {
		return false
	}
	q.data[(q.head+q.count)%int64(len(q.data))] = value
	q.count++
	return true
}

func (q *MyCircularQueue) DeQueue() bool {
	if q.count == 0 {
		return false
	}
	q.head = (q.head + 1) % int64(len(q.data))
	q.count--
	return true
}

func (q *MyCircularQueue) Front() int64 {
	if q.count == 0 {
		return -1
	}
	return q.data[q.head]
}

func (q *MyCircularQueue) Rear() int64 {
	if q.count == 0 {
		return -1
	}
	return q.data[(q.head+q.count-1)%int64(len(q.data))]
}

func (q *MyCircularQueue) IsEmpty() bool { return q.count == 0 }

func (q *MyCircularQueue) IsFull() bool { return q.count == int64(len(q.data)) }

var seed int64 = 622

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func flag(b bool) int64 {
	if b {
		return 1
	}
	return 0
}

func main() {
	const rounds = 300
	ops := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		roll := nextRandom() % 40
		switch {
		case roll < 16:
			ops = append(ops, nextRandom()%1001)
		case roll < 26:
			ops = append(ops, -1)
		case roll < 30:
			ops = append(ops, -2)
		case roll < 34:
			ops = append(ops, -3)
		case roll < 37:
			ops = append(ops, -4)
		default:
			ops = append(ops, -5)
		}
	}
	var checksum int64
	for r := int64(0); r < rounds; r++ {
		q := newQueue(1 + (r*37)%1000)
		for _, op := range ops {
			var v int64
			switch {
			case op >= 0:
				v = flag(q.EnQueue(op))
			case op == -1:
				v = flag(q.DeQueue())
			case op == -2:
				v = q.Front()
			case op == -3:
				v = q.Rear()
			case op == -4:
				v = flag(q.IsEmpty())
			default:
				v = flag(q.IsFull())
			}
			checksum = (checksum*31 + v + 2) % 1000000007
		}
	}
	fmt.Printf("%d queues, %d operations each: checksum %d\n", rounds, len(ops), checksum)
}
