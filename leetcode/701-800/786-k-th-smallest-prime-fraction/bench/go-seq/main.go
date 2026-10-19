// LeetCode 786 — K-th Smallest Prime Fraction: the bench, in Go.
// Mirrors kth_smallest_prime_fraction.kara: a heap of the next fraction
// for each denominator, over the same 64 arrays, with container/heap.
package main

import (
	"container/heap"
	"fmt"
)

type Fraction struct {
	i, j     int
	num, den int64
}

type Heap []Fraction

func (h Heap) Len() int            { return len(h) }
func (h Heap) Less(a, b int) bool  { return h[a].num*h[b].den < h[b].num*h[a].den }
func (h Heap) Swap(a, b int)       { h[a], h[b] = h[b], h[a] }
func (h *Heap) Push(x interface{}) { *h = append(*h, x.(Fraction)) }
func (h *Heap) Pop() interface{} {
	old := *h
	f := old[len(old)-1]
	*h = old[:len(old)-1]
	return f
}

func kthSmallestPrimeFraction(arr []int64, k int64) []int64 {
	n := len(arr)
	h := &Heap{}
	for j := 1; j < n; j++ {
		heap.Push(h, Fraction{0, j, arr[0], arr[j]})
	}
	for t := int64(0); t < k-1; t++ {
		f := heap.Pop(h).(Fraction)
		if f.i+1 < f.j {
			heap.Push(h, Fraction{f.i + 1, f.j, arr[f.i+1], f.den})
		}
	}
	f := heap.Pop(h).(Fraction)
	return []int64{f.num, f.den}
}

var seed int64 = 786

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	composite := make([]bool, 30000)
	primes := []int64{}
	for p := 2; p < 30000; p++ {
		if !composite[p] {
			primes = append(primes, int64(p))
			for m := p * p; m < 30000; m += p {
				composite[m] = true
			}
		}
	}
	arrays := make([][]int64, 0, 64)
	for t := 0; t < 64; t++ {
		taken := make([]bool, len(primes))
		count := 0
		for count < 999 {
			at := nextRandom() % int64(len(primes))
			if !taken[at] {
				taken[at] = true
				count++
			}
		}
		arr := []int64{1}
		for at := range primes {
			if taken[at] {
				arr = append(arr, primes[at])
			}
		}
		arrays = append(arrays, arr)
	}
	const rounds = 64
	var sum, check int64
	for r := 0; r < rounds; r++ {
		hi := nextRandom()
		k := 1 + (hi*32768+nextRandom())%499500
		answer := kthSmallestPrimeFraction(arrays[r%64], k)
		sum += answer[0] + answer[1]
		check = (check*31 + answer[0]*7 + answer[1]) % 1000000007
	}
	fmt.Printf("%d rounds of 1000-number arrays: terms sum to %d, checksum %d\n", rounds, sum, check)
}
