// Benchmark kernel for LeetCode #341 (Flatten Nested List Iterator).
// Mirrors flatten_iterator.kara: a stack of members, with HasNext()
// expanding lists until an integer is on top. 80 rounds, each building a
// pseudo-random nested list of 20,000 top-level members and draining it;
// the sink is a rolling hash of every integer in order.
package main

import "fmt"

type Nested struct {
	isList bool
	v      int64
	items  []Nested
}

type NestedIterator struct {
	stack []Nested
}

func NewNestedIterator(items []Nested) *NestedIterator {
	it := &NestedIterator{}
	it.pushReversed(items)
	return it
}

func (it *NestedIterator) pushReversed(items []Nested) {
	for len(items) > 0 {
		last := len(items) - 1
		it.stack = append(it.stack, items[last])
		items = items[:last]
	}
}

func (it *NestedIterator) HasNext() bool {
	for len(it.stack) > 0 {
		last := len(it.stack) - 1
		top := it.stack[last]
		it.stack = it.stack[:last]
		if !top.isList {
			it.stack = append(it.stack, top)
			return true
		}
		it.pushReversed(top.items)
	}
	return false
}

func (it *NestedIterator) Next() int64 {
	it.HasNext()
	last := len(it.stack) - 1
	if last < 0 || it.stack[last].isList {
		panic("Next() past the end")
	}
	v := it.stack[last].v
	it.stack = it.stack[:last]
	return v
}

func nextRand(state *int64) int64 {
	*state = (*state*1103515245 + 12345) % 2147483648
	return *state >> 8
}

func genMember(state *int64, depth, maxDepth int64) Nested {
	if depth < maxDepth && nextRand(state)%3 == 0 {
		count := nextRand(state) % 5
		var items []Nested
		for k := int64(0); k < count; k++ {
			items = append(items, genMember(state, depth+1, maxDepth))
		}
		return Nested{isList: true, items: items}
	}
	return Nested{v: nextRand(state)%201 - 100}
}

func genList(seed, top, maxDepth int64) []Nested {
	state := seed
	var items []Nested
	for k := int64(0); k < top; k++ {
		items = append(items, genMember(&state, 1, maxDepth))
	}
	return items
}

func main() {
	h := int64(7)
	for r := int64(0); r < 80; r++ {
		it := NewNestedIterator(genList(r*7+1, 20000, 12))
		for it.HasNext() {
			h = (h*31 + it.Next() + 101) % 1000000007
		}
	}
	fmt.Println(h)
}
