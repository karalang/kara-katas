// LeetCode 284 bench mirror — Go. Same eager wrapper and operation mix.
package main

import "fmt"

const N = 200000
const Rounds = 320

type Source struct {
	data  []int64
	pos   int
	pulls int64
}

func (s *Source) hasNext() bool { return s.pos < len(s.data) }
func (s *Source) next() int64 {
	v := s.data[s.pos]
	s.pos++
	s.pulls++
	return v
}

type Peeking struct {
	src  Source
	slot int64
	full bool
}

func makePeeking(data []int64) *Peeking {
	buf := make([]int64, len(data))
	copy(buf, data)
	p := &Peeking{src: Source{data: buf}}
	if p.src.hasNext() {
		p.slot = p.src.next()
		p.full = true
	}
	return p
}
func (p *Peeking) peek() int64   { return p.slot }
func (p *Peeking) hasNext() bool { return p.full }
func (p *Peeking) next() int64 {
	v := p.slot
	if p.src.hasNext() {
		p.slot = p.src.next()
	} else {
		p.full = false
	}
	return v
}

func main() {
	seed := int64(20260823)
	data := make([]int64, N)
	for i := 0; i < N; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		data[i] = seed % 100003
	}
	var sink, total int64
	for r := 0; r < Rounds; r++ {
		p := makePeeking(data)
		var h, pos int64 = 0, 1
		for p.hasNext() {
			h = (h*31 + p.peek()*pos) % 1000000007
			h = (h*31 + p.peek()) % 1000000007
			v := p.next()
			h = (h*31 + v) % 1000000007
			pos++
		}
		total += p.src.pulls
		sink = (sink + h) % 1000000007
	}
	fmt.Println(sink, total)
}
