// Benchmark for #641: mirror of circular_deque.kara (the ★ arm: a ring
// with a start and a count) on the same workload.
package main

import "fmt"

type MyCircularDeque struct {
	data  []int64
	head  int64
	count int64
}

func newDeque(k int64) *MyCircularDeque {
	return &MyCircularDeque{data: make([]int64, k)}
}

func (q *MyCircularDeque) size() int64 { return int64(len(q.data)) }

func (q *MyCircularDeque) insertFront(value int64) bool {
	if q.count == q.size() {
		return false
	}
	q.head = (q.head + q.size() - 1) % q.size()
	q.data[q.head] = value
	q.count++
	return true
}

func (q *MyCircularDeque) insertLast(value int64) bool {
	if q.count == q.size() {
		return false
	}
	at := (q.head + q.count) % q.size()
	q.data[at] = value
	q.count++
	return true
}

func (q *MyCircularDeque) deleteFront() bool {
	if q.count == 0 {
		return false
	}
	q.head = (q.head + 1) % q.size()
	q.count--
	return true
}

func (q *MyCircularDeque) deleteLast() bool {
	if q.count == 0 {
		return false
	}
	q.count--
	return true
}

func (q *MyCircularDeque) getFront() int64 {
	if q.count == 0 {
		return -1
	}
	return q.data[q.head]
}

func (q *MyCircularDeque) getRear() int64 {
	if q.count == 0 {
		return -1
	}
	return q.data[(q.head+q.count-1)%q.size()]
}

func (q *MyCircularDeque) isEmpty() bool { return q.count == 0 }

func (q *MyCircularDeque) isFull() bool { return q.count == q.size() }

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func script(count int64, seed *int64) []int64 {
	ops := []int64{}
	for i := int64(0); i < count; i++ {
		roll := nextRandom(seed) % 40
		switch {
		case roll < 8:
			ops = append(ops, nextRandom(seed)%1001)
		case roll < 16:
			ops = append(ops, 1001+nextRandom(seed)%1001)
		case roll < 21:
			ops = append(ops, -1)
		case roll < 26:
			ops = append(ops, -2)
		case roll < 30:
			ops = append(ops, -3)
		case roll < 34:
			ops = append(ops, -4)
		case roll < 37:
			ops = append(ops, -5)
		default:
			ops = append(ops, -6)
		}
	}
	return ops
}

func flag(b bool) int64 {
	if b {
		return 1
	}
	return 0
}

func main() {
	rounds := int64(300)
	seed := int64(641)
	ops := script(100000, &seed)
	checksum := int64(0)
	for r := int64(0); r < rounds; r++ {
		q := newDeque(1 + (r*37)%1000)
		for _, op := range ops {
			var v int64
			switch {
			case op >= 1001:
				v = flag(q.insertLast(op - 1001))
			case op >= 0:
				v = flag(q.insertFront(op))
			case op == -1:
				v = flag(q.deleteFront())
			case op == -2:
				v = flag(q.deleteLast())
			case op == -3:
				v = q.getFront()
			case op == -4:
				v = q.getRear()
			case op == -5:
				v = flag(q.isEmpty())
			default:
				v = flag(q.isFull())
			}
			checksum = (checksum*31 + v + 2) % 1000000007
		}
	}
	fmt.Printf("%d deques, %d operations each: checksum %d\n", rounds, len(ops), checksum)
}
