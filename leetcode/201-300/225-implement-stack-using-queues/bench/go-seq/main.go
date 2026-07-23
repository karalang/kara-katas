package main

import "fmt"

type Queue struct {
	data []int64
	head int64
}

func qNew() *Queue {
	return &Queue{data: make([]int64, 0, 64), head: 0}
}

func qSize(q *Queue) int64 {
	return int64(len(q.data)) - q.head
}

func qEnqueue(q *Queue, x int64) {
	q.data = append(q.data, x)
}

func qDequeue(q *Queue) int64 {
	v := q.data[q.head]
	q.head++
	return v
}

func qFront(q *Queue) int64 {
	return q.data[q.head]
}

func stackPush(q *Queue, x int64) {
	qEnqueue(q, x)
	rotations := qSize(q) - 1
	for rotations > 0 {
		front := qDequeue(q)
		qEnqueue(q, front)
		rotations--
	}
}

func stackPop(q *Queue) int64 {
	return qDequeue(q)
}

func stackTop(q *Queue) int64 {
	return qFront(q)
}

func main() {
	var passes int64 = 12000
	var opsPerPass int64 = 1500
	var cap int64 = 48
	var modulus int64 = 1000000007

	var state int64 = 12345
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		s := qNew()
		for j := int64(0); j < opsPerPass; j++ {
			state = (state*1103515245 + 12345) & 2147483647
			v := (state % 1000) + 1
			sel := state % 4
			size := qSize(s)
			if size == 0 {
				stackPush(s, v)
			} else if size >= cap {
				if state&1 == 0 {
					sink = (sink + stackPop(s)) % modulus
				} else {
					sink = (sink + stackTop(s)) % modulus
				}
			} else if sel <= 1 {
				stackPush(s, v)
			} else if sel == 2 {
				sink = (sink + stackPop(s)) % modulus
			} else {
				sink = (sink + stackTop(s)) % modulus
			}
		}
	}
	fmt.Println(sink)
}
