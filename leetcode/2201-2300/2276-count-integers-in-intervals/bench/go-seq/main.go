// LeetCode #2276: Count Integers in Intervals -- the bench, the ★ arm.
// Go has no ordered map, so the disjoint intervals live in a treap keyed
// by start, with floor and removal by key.
package main

import "fmt"

type node struct {
	key, value  int64
	prio        uint32
	left, right *node
}

var prioState uint32 = 2463534242

func nextPrio() uint32 {
	prioState ^= prioState << 13
	prioState ^= prioState >> 17
	prioState ^= prioState << 5
	return prioState
}

func split(t *node, key int64) (*node, *node) {
	if t == nil {
		return nil, nil
	}
	if t.key < key {
		l, r := split(t.right, key)
		t.right = l
		return t, r
	}
	l, r := split(t.left, key)
	t.left = r
	return l, t
}

func merge(l, r *node) *node {
	if l == nil {
		return r
	}
	if r == nil {
		return l
	}
	if l.prio > r.prio {
		l.right = merge(l.right, r)
		return l
	}
	r.left = merge(l, r.left)
	return r
}

func insert(t *node, key, value int64) *node {
	n := &node{key: key, value: value, prio: nextPrio()}
	l, r := split(t, key)
	return merge(merge(l, n), r)
}

func erase(t *node, key int64) *node {
	if t == nil {
		return nil
	}
	if t.key == key {
		return merge(t.left, t.right)
	}
	if key < t.key {
		t.left = erase(t.left, key)
	} else {
		t.right = erase(t.right, key)
	}
	return t
}

func floorNode(t *node, key int64) *node {
	var best *node
	for t != nil {
		if t.key <= key {
			best = t
			t = t.right
		} else {
			t = t.left
		}
	}
	return best
}

type countIntervals struct {
	spans *node
	total int64
}

func (c *countIntervals) add(left, right int64) {
	l, r := left, right
	for {
		f := floorNode(c.spans, r)
		if f == nil {
			break
		}
		a, b := f.key, f.value
		if b < l {
			break
		}
		if a < l {
			l = a
		}
		if b > r {
			r = b
		}
		c.total -= b - a + 1
		c.spans = erase(c.spans, a)
	}
	c.total += r - l + 1
	c.spans = insert(c.spans, l, r)
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2276

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	var check int64
	for t := 0; t < 10; t++ {
		span := int64(1000000)
		if t%2 == 0 {
			span = 1000000000
		}
		c := &countIntervals{}
		for i := 0; i < 100000; i++ {
			if nextRandom()%3 == 0 {
				check = (check*31 + c.total) % 1000000007
			} else {
				left := wideRandom()%span + 1
				right := left + wideRandom()%1000
				if right > 1000000000 {
					right = 1000000000
				}
				c.add(left, right)
			}
		}
	}
	fmt.Printf("10 runs of 10^5: checksum %d\n", check)
}
