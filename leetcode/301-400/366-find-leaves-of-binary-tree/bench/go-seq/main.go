// Benchmark for #366 -- mirror of find_leaves.kara. The shared enum is a
// pointer to a node here, nil for the empty tree.
package main

import "fmt"

type Tree struct {
	v           int64
	left, right *Tree
}

type Links struct{ vals, left, right []int64 }

func links(items []int64, present []bool) Links {
	var l Links
	if len(items) == 0 || !present[0] {
		return l
	}
	l.vals = append(l.vals, items[0])
	l.left = append(l.left, -1)
	l.right = append(l.right, -1)
	queue := []int64{0}
	qh := 0
	i := 1
	for i < len(items) {
		if qh == len(queue) {
			break
		}
		parent := queue[qh]
		qh++
		for side := 0; side < 2; side++ {
			if i < len(items) {
				if present[i] {
					id := int64(len(l.vals))
					l.vals = append(l.vals, items[i])
					l.left = append(l.left, -1)
					l.right = append(l.right, -1)
					if side == 0 {
						l.left[parent] = id
					} else {
						l.right[parent] = id
					}
					queue = append(queue, id)
				}
				i++
			}
		}
	}
	return l
}

func build(l *Links, id int64) *Tree {
	if id < 0 {
		return nil
	}
	return &Tree{l.vals[id], build(l, l.left[id]), build(l, l.right[id])}
}

func fileByHeight(t *Tree, out *[][]int64) int64 {
	if t == nil {
		return -1
	}
	h := 1 + max(fileByHeight(t.left, out), fileByHeight(t.right, out))
	if int(h) == len(*out) {
		*out = append(*out, nil)
	}
	(*out)[h] = append((*out)[h], t.v)
	return h
}

func findLeaves(items []int64, present []bool) [][]int64 {
	l := links(items, present)
	var out [][]int64
	if len(l.vals) > 0 {
		fileByHeight(build(&l, 0), &out)
	}
	return out
}

func main() {
	const n = 400000
	var seed int64 = 366
	var checksum, groups int64
	for t := 0; t < 5; t++ {
		items := make([]int64, n)
		present := make([]bool, n)
		for k := int64(0); k < n; k++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			r := seed / 65536
			present[k] = !(k > 0 && r%4 == 0)
			items[k] = r%201 - 100
		}
		for _, group := range findLeaves(items, present) {
			groups++
			for _, v := range group {
				checksum = (checksum*31 + v + 101) % 1000000007
			}
			checksum = (checksum*31 + 7) % 1000000007
		}
	}
	fmt.Printf("%d groups, checksum %d\n", groups, checksum)
}
