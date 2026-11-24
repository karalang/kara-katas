// LeetCode #1298 bench: the ★ arm (a breadth-first walk over the boxes that
// can be opened, each queued once, when it is both held and open) over 100
// cases of 1000 boxes, built once; then 5000 passes, each flipping one box of
// every case between open and locked, chosen from the checksum so far,
// answering it, and folding the answer into the checksum. Go has no deque:
// the queue is a slice read from a moving head.
package main

import "fmt"

func maxCandies(status, candies []int64, keys, containedBoxes [][]int64, initialBoxes []int64) int64 {
	n := len(status)
	open := make([]bool, n)
	for i, s := range status {
		open[i] = s == 1
	}
	held := make([]bool, n)
	queued := make([]bool, n)
	queue := []int64{}
	for _, b := range initialBoxes {
		held[b] = true
		if open[b] && !queued[b] {
			queued[b] = true
			queue = append(queue, b)
		}
	}
	var total int64
	for head := 0; head < len(queue); head++ {
		b := queue[head]
		total += candies[b]
		for _, k := range keys[b] {
			open[k] = true
			if held[k] && !queued[k] {
				queued[k] = true
				queue = append(queue, k)
			}
		}
		for _, c := range containedBoxes[b] {
			held[c] = true
			if open[c] && !queued[c] {
				queued[c] = true
				queue = append(queue, c)
			}
		}
	}
	return total
}

var seed int64 = 1298

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type Case struct {
	status, candies, initial []int64
	keys, contained          [][]int64
}

func contains(v []int64, x int64) bool {
	for _, y := range v {
		if y == x {
			return true
		}
	}
	return false
}

func makeCase(n, open, initialIn, nest, maxKeys int64) Case {
	order := make([]int64, n)
	for i := range order {
		order[i] = int64(i)
	}
	for i := int64(0); i < n; i++ {
		j := i + nextRandom()%(n-i)
		order[i], order[j] = order[j], order[i]
	}
	c := Case{status: make([]int64, n), candies: make([]int64, n), keys: make([][]int64, n), contained: make([][]int64, n), initial: []int64{}}
	for i := int64(0); i < n; i++ {
		b := order[i]
		roll := nextRandom() % 100
		if i > 0 && roll < nest {
			parent := order[nextRandom()%i]
			c.contained[parent] = append(c.contained[parent], b)
		} else if nextRandom()%100 < initialIn {
			c.initial = append(c.initial, b)
		}
		if nextRandom()%100 < open {
			c.status[b] = 1
		}
		c.candies[b] = 1 + nextRandom()%1000
		count := nextRandom() % (maxKeys + 1)
		for j := int64(0); j < count; j++ {
			k := nextRandom() % n
			if !contains(c.keys[b], k) {
				c.keys[b] = append(c.keys[b], k)
			}
		}
	}
	return c
}

func main() {
	cases := []Case{}
	for t := int64(0); t < 100; t++ {
		cases = append(cases, makeCase(1000, 10+t%40, 5+t%20, 60+t%40, 1+t%4))
	}
	var check int64
	for p := int64(0); p < 5000; p++ {
		for t := range cases {
			c := &cases[t]
			b := check % 1000
			c.status[b] = 1 - c.status[b]
			got := maxCandies(c.status, c.candies, c.keys, c.contained, c.initial)
			check = (check*31 + got + p) % 1000000007
		}
	}
	fmt.Printf("5000 passes over 100 cases of 1000 boxes: checksum %d\n", check)
}
