package main

import "fmt"

type MyQueue struct {
	inbox  []int64
	outbox []int64
}

func newQueue() *MyQueue {
	return &MyQueue{inbox: make([]int64, 0), outbox: make([]int64, 0)}
}

func (q *MyQueue) push(x int64) {
	q.inbox = append(q.inbox, x)
}

func (q *MyQueue) refill() {
	if len(q.outbox) == 0 {
		for len(q.inbox) > 0 {
			v := q.inbox[len(q.inbox)-1]
			q.inbox = q.inbox[:len(q.inbox)-1]
			q.outbox = append(q.outbox, v)
		}
	}
}

func (q *MyQueue) pop() int64 {
	q.refill()
	v := q.outbox[len(q.outbox)-1]
	q.outbox = q.outbox[:len(q.outbox)-1]
	return v
}

func (q *MyQueue) peek() int64 {
	q.refill()
	return q.outbox[len(q.outbox)-1]
}

func (q *MyQueue) empty() bool {
	return len(q.inbox) == 0 && len(q.outbox) == 0
}

func main() {
	var n int64 = 75000000
	var cap int64 = 4096
	var mask int64 = 1048575

	q := newQueue()
	var sz int64 = 0
	var sink int64 = 0
	var state int64 = 12345

	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		if q.empty() || (state%2 == 0 && sz < cap) {
			q.push(state & mask)
			sz += 1
		} else if state%4 == 0 {
			sink += q.peek()
		} else {
			sink += q.pop()
			sz -= 1
		}
	}
	fmt.Println(sink)
}
