// LeetCode #2233: Maximum Product After K Increments -- the benchmark's
// Go mirror of product.kara: the smallest raised k times through a binary
// min-heap, then the heap emptied into the product.
package main

import "fmt"

type minHeap []int64

func (h *minHeap) push(x int64) {
	*h = append(*h, x)
	a := *h
	i := len(a) - 1
	for i > 0 {
		parent := (i - 1) / 2
		if a[parent] <= a[i] {
			break
		}
		a[parent], a[i] = a[i], a[parent]
		i = parent
	}
}

func (h *minHeap) pop() int64 {
	a := *h
	top := a[0]
	n := len(a) - 1
	a[0] = a[n]
	a = a[:n]
	*h = a
	i := 0
	for {
		l, r, m := 2*i+1, 2*i+2, i
		if l < n && a[l] < a[m] {
			m = l
		}
		if r < n && a[r] < a[m] {
			m = r
		}
		if m == i {
			break
		}
		a[m], a[i] = a[i], a[m]
		i = m
	}
	return top
}

func maximumProduct(nums []int64, k int64) int64 {
	queue := make(minHeap, 0, len(nums))
	for _, x := range nums {
		queue.push(x)
	}
	for j := int64(0); j < k; j++ {
		smallest := queue.pop()
		queue.push(smallest + 1)
	}
	product := int64(1)
	for len(queue) > 0 {
		product = product * queue.pop() % 1000000007
	}
	return product
}

var seed int64 = 2233

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	nums := make([]int64, 20000)
	for i := range nums {
		nums[i] = wideRandom() % 1000001
	}
	check := int64(0)
	for pass := 0; pass < 150; pass++ {
		// punch: one number drawn again before each pass
		at := nextRandom() % 20000
		nums[at] = wideRandom() % 1000001
		check = (check*31 + maximumProduct(nums, 50000)) % 1000000007
	}
	fmt.Printf("150 passes over 20000 numbers, k = 50000: checksum %d\n", check)
}
