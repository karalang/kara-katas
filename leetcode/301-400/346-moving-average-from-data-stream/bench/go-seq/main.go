// Benchmark workload for LeetCode #346 — Go mirror of moving_average.kara.
//
// Go has no standard deque either (container/list is a linked list, a
// different structure), so the window is the same growable ring deque the C
// mirror uses.
package main

import "fmt"

const (
	LEN    = 10000000
	WINDOW = 1000
)

type Deque struct {
	buf          []int64
	head, length int
}

func (d *Deque) PushBack(v int64) {
	if d.length == len(d.buf) {
		c := len(d.buf) * 2
		if c == 0 {
			c = 4
		}
		nb := make([]int64, c)
		for k := 0; k < d.length; k++ {
			nb[k] = d.buf[(d.head+k)%len(d.buf)]
		}
		d.buf = nb
		d.head = 0
	}
	d.buf[(d.head+d.length)%len(d.buf)] = v
	d.length++
}

func (d *Deque) PopFront() int64 {
	v := d.buf[d.head]
	d.head = (d.head + 1) % len(d.buf)
	d.length--
	return v
}

type MovingAverage struct {
	size   int
	window Deque
	sum    int64
}

func (m *MovingAverage) Next(val int64) float64 {
	m.window.PushBack(val)
	m.sum += val
	if m.window.length > m.size {
		m.sum -= m.window.PopFront()
	}
	return float64(m.sum) / float64(m.window.length)
}

func main() {
	m := MovingAverage{size: WINDOW}
	seed := int64(346)
	sink := 0.0
	for i := 0; i < LEN; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		sink += m.Next(seed/16%200001 - 100000)
	}
	fmt.Printf("sink %.3f\n", sink)
}
