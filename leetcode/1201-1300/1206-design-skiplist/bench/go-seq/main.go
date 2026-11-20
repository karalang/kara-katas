// LeetCode #1206 bench, in Go: the ★ arm (a skiplist whose nodes live in a
// slice, each node's forward links one per level it stands on, heights by
// coin flips from the list's own generator, erased slots reused) on 50000
// calls drawn once, a third each of search, add and erase, on values up to
// 20000; then 10 rounds, each on a new list, every answer folded into a
// checksum.
package main

import "fmt"

const levels = 16

type Skiplist struct {
	values []int64
	next   [][]int
	free   []int
	seed   int64
}

func newSkiplist() *Skiplist {
	head := make([]int, levels)
	for i := range head {
		head[i] = -1
	}
	return &Skiplist{values: []int64{0}, next: [][]int{head}, seed: 1206}
}

func (s *Skiplist) height() int {
	h := 1
	for h < levels {
		s.seed = (s.seed*1103515245 + 12345) % 2147483648
		if (s.seed/65536)%2 == 1 {
			break
		}
		h++
	}
	return h
}

func (s *Skiplist) path(target int64) [levels]int {
	var path [levels]int
	x := 0
	for level := levels - 1; level >= 0; level-- {
		for s.next[x][level] >= 0 && s.values[s.next[x][level]] < target {
			x = s.next[x][level]
		}
		path[level] = x
	}
	return path
}

func (s *Skiplist) search(target int64) bool {
	at := s.next[s.path(target)[0]][0]
	return at >= 0 && s.values[at] == target
}

func (s *Skiplist) add(num int64) {
	path := s.path(num)
	h := s.height()
	links := make([]int, h)
	for level := 0; level < h; level++ {
		links[level] = s.next[path[level]][level]
	}
	var node int
	if n := len(s.free); n > 0 {
		node = s.free[n-1]
		s.free = s.free[:n-1]
		s.values[node] = num
		s.next[node] = links
	} else {
		s.values = append(s.values, num)
		s.next = append(s.next, links)
		node = len(s.values) - 1
	}
	for level := 0; level < h; level++ {
		s.next[path[level]][level] = node
	}
}

func (s *Skiplist) erase(num int64) bool {
	path := s.path(num)
	at := s.next[path[0]][0]
	if at < 0 || s.values[at] != num {
		return false
	}
	for level := 0; level < len(s.next[at]); level++ {
		if s.next[path[level]][level] == at {
			s.next[path[level]][level] = s.next[at][level]
		}
	}
	s.free = append(s.free, at)
	return true
}

var seed int64 = 1206

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type call struct{ op, v int64 }
	calls := make([]call, 0, 50000)
	for k := 0; k < 50000; k++ {
		op := nextRandom() % 3
		hi := nextRandom()
		calls = append(calls, call{op, (hi*32768 + nextRandom()) % 20001})
	}
	var check int64
	for round := 0; round < 10; round++ {
		s := newSkiplist()
		for _, c := range calls {
			var answer bool
			switch c.op {
			case 0:
				answer = s.search(c.v)
			case 1:
				s.add(c.v)
				answer = true
			default:
				answer = s.erase(c.v)
			}
			a := int64(0)
			if answer {
				a = 1
			}
			check = (check*131 + c.op*2 + a) % 1000000007
		}
	}
	fmt.Printf("10 rounds of 50000 calls: checksum %d\n", check)
}
