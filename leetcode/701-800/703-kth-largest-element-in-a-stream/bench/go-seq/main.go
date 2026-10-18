// LeetCode #703 bench: the heap arm in Go. See the .kara twin for the
// workload.
package main

import "fmt"

type KthLargest struct {
	k    int
	heap []int64
}

func newKthLargest(k int, nums []int64) *KthLargest {
	s := &KthLargest{k: k}
	for _, x := range nums {
		s.add(x)
	}
	return s
}

func (s *KthLargest) add(val int64) int64 {
	h := s.heap
	if len(h) < s.k {
		h = append(h, val)
		i := len(h) - 1
		for i > 0 {
			parent := (i - 1) / 2
			if h[parent] <= h[i] {
				break
			}
			h[parent], h[i] = h[i], h[parent]
			i = parent
		}
		s.heap = h
	} else if val > h[0] {
		h[0] = val
		n := len(h)
		i := 0
		for {
			left := 2*i + 1
			right := left + 1
			least := i
			if left < n && h[left] < h[least] {
				least = left
			}
			if right < n && h[right] < h[least] {
				least = right
			}
			if least == i {
				break
			}
			h[least], h[i] = h[i], h[least]
			i = least
		}
	}
	return s.heap[0]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(703)
	checksum := int64(0)
	changes := 0
	for round := 0; round < 5; round++ {
		for stream := 0; stream < 10; stream++ {
			k := 50 * (stream + 1)
			price := int64(100000)
			nums := make([]int64, 0)
			for i := 0; i < 1000; i++ {
				price += nextRandom(&seed)%201 - 90
				nums = append(nums, price)
			}
			s := newKthLargest(k, nums)
			last := int64(0)
			for i := 0; i < 200000; i++ {
				price += nextRandom(&seed)%201 - 90
				answer := s.add(price)
				if answer != last {
					changes++
				}
				last = answer
				checksum = (checksum*31 + answer) % 1000000007
			}
		}
	}
	fmt.Printf("5 rounds of 10 streams of 200000 prices: answer changed %d times, checksum %d\n", changes, checksum)
}
