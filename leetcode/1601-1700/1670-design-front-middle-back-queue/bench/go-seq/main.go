// LeetCode #1670: Design Front Middle Back Queue -- the bench's Go mirror:
// the ★ arm on one run of 1000000 calls, a push three times in five,
// values up to 10^9, drawn first and then replayed 60 times, each on a new
// queue. Go has no deque, so each half is a growable ring buffer, as
// Rust's and Kāra's `VecDeque` are.
package main

import "fmt"

type Deque struct {
	buf       []int32
	head, len int
}

func (d *Deque) grow() {
	c := len(d.buf) * 2
	if c == 0 {
		c = 8
	}
	buf := make([]int32, c)
	for i := 0; i < d.len; i++ {
		buf[i] = d.buf[(d.head+i)%len(d.buf)]
	}
	d.buf = buf
	d.head = 0
}

func (d *Deque) pushFront(v int32) {
	if d.len == len(d.buf) {
		d.grow()
	}
	d.head = (d.head + len(d.buf) - 1) % len(d.buf)
	d.buf[d.head] = v
	d.len++
}

func (d *Deque) pushBack(v int32) {
	if d.len == len(d.buf) {
		d.grow()
	}
	d.buf[(d.head+d.len)%len(d.buf)] = v
	d.len++
}

func (d *Deque) popFront() int32 {
	v := d.buf[d.head]
	d.head = (d.head + 1) % len(d.buf)
	d.len--
	return v
}

func (d *Deque) popBack() int32 {
	d.len--
	return d.buf[(d.head+d.len)%len(d.buf)]
}

type FrontMiddleBackQueue struct {
	front, back Deque
}

func (q *FrontMiddleBackQueue) balance() {
	if q.front.len > q.back.len {
		q.back.pushFront(q.front.popBack())
	} else if q.back.len > q.front.len+1 {
		q.front.pushBack(q.back.popFront())
	}
}

func (q *FrontMiddleBackQueue) PushFront(v int32) {
	q.front.pushFront(v)
	q.balance()
}

func (q *FrontMiddleBackQueue) PushMiddle(v int32) {
	q.front.pushBack(v)
	q.balance()
}

func (q *FrontMiddleBackQueue) PushBack(v int32) {
	q.back.pushBack(v)
	q.balance()
}

func (q *FrontMiddleBackQueue) PopFront() int32 {
	var v int32
	if q.front.len > 0 {
		v = q.front.popFront()
	} else if q.back.len > 0 {
		v = q.back.popFront()
	} else {
		return -1
	}
	q.balance()
	return v
}

func (q *FrontMiddleBackQueue) PopMiddle() int32 {
	var v int32
	if q.front.len == q.back.len {
		if q.front.len == 0 {
			return -1
		}
		v = q.front.popBack()
	} else {
		v = q.back.popFront()
	}
	q.balance()
	return v
}

func (q *FrontMiddleBackQueue) PopBack() int32 {
	if q.back.len == 0 {
		return -1
	}
	v := q.back.popBack()
	q.balance()
	return v
}

var seed int64 = 1670

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds = 60
	const calls = 1000000
	ops := make([]int64, calls)
	vals := make([]int32, calls)
	for i := range ops {
		r := nextRandom() % 10
		if r < 6 {
			ops[i] = r / 2
		} else {
			ops[i] = r - 3
		}
		vals[i] = int32((nextRandom()*32768+nextRandom())%1000000000 + 1)
	}
	var empty, left, check int64
	for round := 0; round < rounds; round++ {
		q := &FrontMiddleBackQueue{}
		for i, op := range ops {
			var got int32
			switch op {
			case 0:
				q.PushFront(vals[i])
				continue
			case 1:
				q.PushMiddle(vals[i])
				continue
			case 2:
				q.PushBack(vals[i])
				continue
			case 3:
				got = q.PopFront()
			case 4:
				got = q.PopMiddle()
			default:
				got = q.PopBack()
			}
			if got == -1 {
				empty++
			}
			check = (check*31 + int64(got) + 1) % 1000000007
		}
		left += int64(q.front.len + q.back.len)
	}
	fmt.Printf("%d calls, %d rounds: %d pops on an empty queue, %d values left, checksum %d\n", calls, rounds, empty, left, check)
}
