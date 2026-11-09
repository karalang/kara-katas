// LeetCode #2034: Stock Price Fluctuation -- the ★ arm in Go, the same
// algorithm and workload as stock.kara: a map of prices, the latest
// timestamp, and two binary heaps of (price, timestamp) records with stale
// ones popped at query time.
package main

import "fmt"

type rec struct{ price, ts int64 }

type heap struct {
	a        []rec
	maxFirst bool
}

func (h *heap) before(x, y rec) bool {
	if h.maxFirst {
		return x.price > y.price || (x.price == y.price && x.ts > y.ts)
	}
	return x.price < y.price || (x.price == y.price && x.ts < y.ts)
}

func (h *heap) push(r rec) {
	h.a = append(h.a, r)
	i := len(h.a) - 1
	for i > 0 {
		p := (i - 1) / 2
		if !h.before(r, h.a[p]) {
			break
		}
		h.a[i] = h.a[p]
		i = p
	}
	h.a[i] = r
}

func (h *heap) pop() {
	n := len(h.a) - 1
	last := h.a[n]
	h.a = h.a[:n]
	i := 0
	for {
		c := 2*i + 1
		if c >= n {
			break
		}
		if c+1 < n && h.before(h.a[c+1], h.a[c]) {
			c++
		}
		if !h.before(h.a[c], last) {
			break
		}
		h.a[i] = h.a[c]
		i = c
	}
	if n > 0 {
		h.a[i] = last
	}
}

type stockPrice struct {
	prices      map[int64]int64
	latest      int64
	highs, lows heap
}

func newStock() *stockPrice {
	return &stockPrice{prices: map[int64]int64{}, highs: heap{maxFirst: true}}
}

func (s *stockPrice) update(ts, price int64) {
	s.prices[ts] = price
	if ts > s.latest {
		s.latest = ts
	}
	s.highs.push(rec{price, ts})
	s.lows.push(rec{price, ts})
}

func (s *stockPrice) extreme(h *heap) int64 {
	for {
		r := h.a[0]
		if s.prices[r.ts] == r.price {
			return r.price
		}
		h.pop()
	}
}

var seed int64 = 2034

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type op struct{ kind, ts, price int64 }

func main() {
	spans := []int64{1000000000, 100000, 1000, 1000000000, 50000}
	tops := []int64{1000000000, 1000, 1000000000, 100, 1000000}
	sessions := make([][]op, 10)
	for a := 0; a < 10; a++ {
		span, top, upd := spans[a%5], tops[a%5], int64(a%7+2)
		ops := make([]op, 0, 100000)
		for i := 0; i < 100000; i++ {
			if i == 0 || nextRandom()%10 < upd {
				hi := nextRandom()
				lo := nextRandom()
				ts := (hi*32768+lo)%span + 1
				hi = nextRandom()
				lo = nextRandom()
				price := (hi*32768+lo)%top + 1
				ops = append(ops, op{0, ts, price})
			} else {
				ops = append(ops, op{nextRandom()%3 + 1, 0, 0})
			}
		}
		sessions[a] = ops
	}
	var runs, queries, check int64
	for round := 0; round < 15; round++ {
		for _, ops := range sessions {
			s := newStock()
			for _, o := range ops {
				if o.kind == 0 {
					s.update(o.ts, o.price)
					continue
				}
				var answer int64
				switch o.kind {
				case 1:
					answer = s.prices[s.latest]
				case 2:
					answer = s.extreme(&s.highs)
				default:
					answer = s.extreme(&s.lows)
				}
				queries++
				check = (check*31 + answer%1000000007 + o.kind) % 1000000007
			}
			runs++
		}
	}
	fmt.Printf("%d sessions: %d queries, checksum %d\n", runs, queries, check)
}
