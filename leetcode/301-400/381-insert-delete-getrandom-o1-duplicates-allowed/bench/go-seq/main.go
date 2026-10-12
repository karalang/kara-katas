// Benchmark mirror of randomized_collection.kara (#381): a slice of
// elements, a map from each value to its positions, and each position's
// index in its value's list.
package main

import "fmt"

type RandomizedCollection struct {
	vals      []int64
	slot      []int64
	positions map[int64][]int64
	seed      int64
}

func newCollection() *RandomizedCollection {
	return &RandomizedCollection{positions: map[int64][]int64{}, seed: 381}
}

func (c *RandomizedCollection) insert(val int64) bool {
	p := int64(len(c.vals))
	c.vals = append(c.vals, val)
	list := c.positions[val]
	c.slot = append(c.slot, int64(len(list)))
	list = append(list, p)
	c.positions[val] = list
	return len(list) == 1
}

func (c *RandomizedCollection) remove(val int64) bool {
	list, ok := c.positions[val]
	if !ok {
		return false
	}
	p := list[len(list)-1]
	list = list[:len(list)-1]
	if len(list) == 0 {
		delete(c.positions, val)
	} else {
		c.positions[val] = list
	}
	last := int64(len(c.vals)) - 1
	if p < last {
		moved := c.vals[last]
		k := c.slot[last]
		c.vals[p] = moved
		c.slot[p] = k
		c.positions[moved][k] = p
	}
	c.vals = c.vals[:last]
	c.slot = c.slot[:last]
	return true
}

func (c *RandomizedCollection) getRandom() int64 {
	c.seed = (c.seed*1103515245 + 12345) % 2147483648
	return c.vals[(c.seed/65536)%int64(len(c.vals))]
}

func main() {
	rc := newCollection()
	seed := int64(381)
	checksum := int64(0)
	for i := 0; i < 20000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		op := (seed / 65536) % 3
		seed = (seed*1103515245 + 12345) % 2147483648
		x := (seed / 64) % 100000
		var v int64
		if op == 0 {
			if rc.insert(x) {
				v = 1
			}
		} else if op == 1 {
			if rc.remove(x) {
				v = 1
			}
		} else if len(rc.vals) > 0 {
			v = rc.getRandom() + 2
		} else {
			v = 7
		}
		checksum = (checksum*31 + v) % 1000000007
	}
	fmt.Printf("checksum %d size %d\n", checksum, len(rc.vals))
}
