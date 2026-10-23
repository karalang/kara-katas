// LeetCode #912: Sort an Array -- bench program, Go.
//
// Heap sort on 500,000 numbers from -5 * 10^4 to 5 * 10^4, built once.
// Each round sorts a copy, folds a sample of the sorted values into a
// checksum and changes one number; 6 rounds.
package main

import "fmt"

func siftDown(a []int64, start, end int) {
	root := start
	for {
		child := 2*root + 1
		if child >= end {
			return
		}
		if child+1 < end && a[child+1] > a[child] {
			child++
		}
		if a[root] >= a[child] {
			return
		}
		a[root], a[child] = a[child], a[root]
		root = child
	}
}

func sortArray(nums []int64) []int64 {
	a := append([]int64(nil), nums...)
	n := len(a)
	for parent := n/2 - 1; parent >= 0; parent-- {
		siftDown(a, parent, n)
	}
	for end := n - 1; end > 0; end-- {
		a[0], a[end] = a[end], a[0]
		siftDown(a, 0, end)
	}
	return a
}

var seed int64 = 912

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := 500000
	rounds := 6
	nums := make([]int64, n)
	for i := range nums {
		nums[i] = nextRandom()%100001 - 50000
	}
	var check int64
	for round := 0; round < rounds; round++ {
		sorted := sortArray(nums)
		for i := round; i < n; i += 997 {
			check = (check*31 + sorted[i] + 50000) % 1000000007
		}
		nums[round*7919%n] = nextRandom()%100001 - 50000
	}
	fmt.Printf("%d rounds over %d numbers: checksum %d\n", rounds, n, check)
}
