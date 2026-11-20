// LeetCode #2363: Merge Similar Items -- the bench, the ★ arm in Go: every
// item of both lists added into a sorted map from value to total weight,
// which walks out in order of value. Go has no ordered map, so the totals
// live in a treap keyed by value, with insert-or-add and an in-order walk.
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

func rotateRight(t *node) *node {
	l := t.left
	t.left = l.right
	l.right = t
	return l
}

func rotateLeft(t *node) *node {
	r := t.right
	t.right = r.left
	r.left = t
	return r
}

// add adds weight to key's total, inserting key at 0 first if it is missing
func add(t *node, key, weight int64) *node {
	if t == nil {
		return &node{key: key, value: weight, prio: nextPrio()}
	}
	if key == t.key {
		t.value += weight
	} else if key < t.key {
		t.left = add(t.left, key, weight)
		if t.left.prio > t.prio {
			t = rotateRight(t)
		}
	} else {
		t.right = add(t.right, key, weight)
		if t.right.prio > t.prio {
			t = rotateLeft(t)
		}
	}
	return t
}

func walk(t *node, out [][]int64) [][]int64 {
	if t == nil {
		return out
	}
	out = walk(t.left, out)
	out = append(out, []int64{t.key, t.value})
	return walk(t.right, out)
}

func mergeSimilarItems(items1, items2 [][]int64) [][]int64 {
	var totals *node
	for _, item := range items1 {
		totals = add(totals, item[0], item[1])
	}
	for _, item := range items2 {
		totals = add(totals, item[0], item[1])
	}
	return walk(totals, nil)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomItems(seed *int64, count int64) [][]int64 {
	// count distinct values from 1 to 1000 in a shuffled order, each with
	// a weight of 1 to 1000
	values := make([]int64, 1000)
	for i := range values {
		values[i] = int64(i + 1)
	}
	for i := int64(999); i >= 1; i-- {
		j := nextRandom(seed) % (i + 1)
		values[i], values[j] = values[j], values[i]
	}
	items := make([][]int64, count)
	for i := range items {
		items[i] = []int64{values[i], 1 + nextRandom(seed)%1000}
	}
	return items
}

func main() {
	// pair a: lists of 100 (a + 1) and 1000 - 50 a items
	seed := int64(2363)
	firsts := make([][][]int64, 10)
	seconds := make([][][]int64, 10)
	for a := int64(0); a < 10; a++ {
		firsts[a] = randomItems(&seed, 100*(a+1))
		seconds[a] = randomItems(&seed, 1000-50*a)
	}
	check := int64(0)
	for p := int64(0); p < 400; p++ {
		for a := 0; a < 10; a++ {
			merged := mergeSimilarItems(firsts[a], seconds[a])
			last := merged[len(merged)-1]
			check = (check*31 + int64(len(merged))*1009 + last[1] + p) % 1000000007
		}
	}
	fmt.Printf("400 passes over 10 pairs of lists: checksum %d\n", check)
}
