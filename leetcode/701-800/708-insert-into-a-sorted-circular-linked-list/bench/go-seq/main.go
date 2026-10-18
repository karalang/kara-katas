// LeetCode #708: Insert into a Sorted Circular Linked List -- an arena.
// Benchmark mirror of the Kara star arm: values and next links in two
// growable slices; walk from the given node to the first gap that fits.
package main

import (
	"fmt"
	"sort"
)

type Ring struct {
	vals []int64
	next []int64
}

func fits(a, b, x int64) bool {
	if a <= b {
		return a <= x && x <= b
	}
	return x >= a || x <= b
}

// Insert takes head -1 for an empty list.
func (r *Ring) Insert(head, insertVal int64) int64 {
	id := int64(len(r.vals))
	r.vals = append(r.vals, insertVal)
	if head < 0 {
		r.next = append(r.next, id)
		return id
	}
	prev := head
	for {
		curr := r.next[prev]
		if fits(r.vals[prev], r.vals[curr], insertVal) {
			break
		}
		prev = curr
		if prev == head {
			break
		}
	}
	r.next = append(r.next, r.next[prev])
	r.next[prev] = id
	return head
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(708)
	checksum := int64(0)
	n := int64(20000)
	for round := 0; round < 5; round++ {
		for ringNo := 0; ringNo < 10; ringNo++ {
			sorted := make([]int64, n)
			for i := range sorted {
				hi := nextRandom(&seed)
				lo := nextRandom(&seed)
				sorted[i] = (hi*32768+lo)%2000001 - 1000000
			}
			sort.Slice(sorted, func(i, j int) bool { return sorted[i] < sorted[j] })
			start := nextRandom(&seed) % n
			ring := &Ring{}
			for i := int64(0); i < n; i++ {
				ring.vals = append(ring.vals, sorted[(start+i)%n])
				ring.next = append(ring.next, (i+1)%n)
			}
			head := int64(0)
			for i := 0; i < 1000; i++ {
				hi := nextRandom(&seed)
				lo := nextRandom(&seed)
				head = ring.Insert(head, (hi*32768+lo)%2000001-1000000)
			}
			at := head
			for {
				checksum = (checksum*31 + ring.vals[at] + 1000001) % 1000000007
				at = ring.next[at]
				if at == head {
					break
				}
			}
		}
	}
	fmt.Printf("5 rounds of 10 rings of 20000 values, 1000 inserts each: checksum %d\n", checksum)
}
