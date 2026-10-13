// Benchmark for #460: mirror of lfu_cache.kara (the ★ arm, a linked list
// per use count) on the same workload.
package main

import "fmt"

type node struct {
	key, value, count int64
	prev, next        int
}

type lfuCache struct {
	capacity  int
	nodes     []node
	index     map[int64]int
	sentinels map[int64]int
	least     int64
	free      int
}

func newLFUCache(capacity int) *lfuCache {
	return &lfuCache{capacity: capacity, index: map[int64]int{}, sentinels: map[int64]int{}, free: -1}
}

func (c *lfuCache) unlink(i int) {
	prev, next := c.nodes[i].prev, c.nodes[i].next
	c.nodes[prev].next = next
	c.nodes[next].prev = prev
}

func (c *lfuCache) appendTo(i int, count int64) {
	s, ok := c.sentinels[count]
	if !ok {
		s = len(c.nodes)
		c.nodes = append(c.nodes, node{key: -1, count: count, prev: s, next: s})
		c.sentinels[count] = s
	}
	last := c.nodes[s].prev
	c.nodes[i].count = count
	c.nodes[i].prev = last
	c.nodes[i].next = s
	c.nodes[last].next = i
	c.nodes[s].prev = i
}

func (c *lfuCache) isEmpty(count int64) bool {
	s := c.sentinels[count]
	return c.nodes[s].next == s
}

func (c *lfuCache) touch(i int) {
	count := c.nodes[i].count
	c.unlink(i)
	if c.least == count && c.isEmpty(count) {
		c.least = count + 1
	}
	c.appendTo(i, count+1)
}

func (c *lfuCache) get(key int64) int64 {
	i, ok := c.index[key]
	if !ok {
		return -1
	}
	c.touch(i)
	return c.nodes[i].value
}

func (c *lfuCache) put(key, value int64) {
	if c.capacity == 0 {
		return
	}
	if i, ok := c.index[key]; ok {
		c.nodes[i].value = value
		c.touch(i)
		return
	}
	if len(c.index) == c.capacity {
		s := c.sentinels[c.least]
		victim := c.nodes[s].next
		c.unlink(victim)
		delete(c.index, c.nodes[victim].key)
		c.free = victim
	}
	var i int
	if c.free >= 0 {
		i = c.free
		c.free = -1
		c.nodes[i].key = key
		c.nodes[i].value = value
	} else {
		c.nodes = append(c.nodes, node{key: key, value: value, prev: -1, next: -1})
		i = len(c.nodes) - 1
	}
	c.index[key] = i
	c.appendTo(i, 1)
	c.least = 1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const capacity = 4096
	const calls = 10000000
	seed := int64(460)
	cache := newLFUCache(capacity)
	hits := 0
	checksum := int64(0)
	for n := 0; n < calls; n++ {
		a := nextRandom(&seed) % 200
		b := nextRandom(&seed) % 200
		key := a * b
		if nextRandom(&seed)%2 == 0 {
			cache.put(key, nextRandom(&seed)%1000000)
		} else {
			answer := cache.get(key)
			if answer >= 0 {
				hits++
			}
			checksum = (checksum*31 + answer + 2) % 1000000007
		}
	}
	fmt.Printf("%d calls on a cache of %d: %d hits, checksum %d\n", calls, capacity, hits, checksum)
}
