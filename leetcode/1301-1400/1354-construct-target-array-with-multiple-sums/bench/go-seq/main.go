// LeetCode #1354 bench -- Go: the moves undone from the target, largest
// value first, in a binary max-heap with a running total, many undos of
// one value as one remainder.
package main

import "fmt"

type maxHeap []int64

func (h *maxHeap) push(v int64) {
	*h = append(*h, v)
	a := *h
	i := len(a) - 1
	for i > 0 {
		p := (i - 1) / 2
		if a[p] >= a[i] {
			break
		}
		a[p], a[i] = a[i], a[p]
		i = p
	}
}

func (h *maxHeap) pop() int64 {
	a := *h
	top := a[0]
	last := len(a) - 1
	a[0] = a[last]
	a = a[:last]
	i := 0
	for {
		l, r, m := 2*i+1, 2*i+2, i
		if l < len(a) && a[l] > a[m] {
			m = l
		}
		if r < len(a) && a[r] > a[m] {
			m = r
		}
		if m == i {
			break
		}
		a[m], a[i] = a[i], a[m]
		i = m
	}
	*h = a
	return top
}

func isPossible(target []int32, heap *maxHeap) bool {
	if len(target) == 1 {
		return target[0] == 1
	}
	var total int64
	*heap = (*heap)[:0]
	for _, x := range target {
		total += int64(x)
		heap.push(int64(x))
	}
	for {
		x := heap.pop()
		rest := total - x
		if x == 1 || rest == 1 {
			return true
		}
		if x <= rest || x%rest == 0 {
			return false
		}
		before := x % rest
		heap.push(before)
		total = rest + before
	}
}

var seed int64 = 1354

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func reached(n, moves, top int64) []int32 {
	arr := make([]int64, n)
	for i := range arr {
		arr[i] = 1
	}
	total := n
	for m := int64(0); m < moves; m++ {
		if total > top {
			break
		}
		i := nextRandom() % n
		was := arr[i]
		arr[i] = total
		total = 2*total - was
	}
	out := make([]int32, n)
	for i, x := range arr {
		out[i] = int32(x)
	}
	return out
}

func main() {
	// 20 targets of 5 * 10^4 values, each reached from the ones by moves
	// until a value would pass 10^9, built once; then 2000 rounds, each
	// changing one place of one target, drawn from the checksum so far,
	// answering, and putting the place back; one round in four leaves the
	// value as it was
	targets := make([][]int32, 20)
	for k := range targets {
		targets[k] = reached(50000, 100, 1000000000)
	}
	heap := make(maxHeap, 0, 50000)
	var check int64
	for r := int64(0); r < 2000; r++ {
		k := check % 20
		at := (check / 20) % 50000
		was := targets[k][at]
		if r%4 != 0 {
			targets[k][at] = was + 1 + int32((check/7)%3)
		}
		var got int64
		if isPossible(targets[k], &heap) {
			got = 1
		}
		targets[k][at] = was
		check = (check*31 + got*1000 + r) % 1000000007
	}
	fmt.Printf("2000 rounds over 20 targets of 5 * 10^4 values: checksum %d\n", check)
}
