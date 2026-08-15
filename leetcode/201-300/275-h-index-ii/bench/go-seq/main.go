// Benchmark workload for LeetCode #275 — H-Index II.
//
// Algorithm-for-algorithm mirror of ../hsearch.kara. See that file's header for
// what this lane measures and why the array is sized at 2 MiB.
package main

import "fmt"

func hIndexPrefix(citations []int64, n int64) int64 {
	var lo int64 = 0
	hi := n
	for lo < hi {
		mid := lo + (hi-lo)/2
		if citations[mid] >= n-mid {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return n - lo
}

func main() {
	const size int64 = 262144
	const queries int64 = 6000000

	citations := make([]int64, 0, size)
	var state int64 = 275275
	var cur int64 = 0
	for i := int64(0); i < size; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		cur += (state / 256) % 3
		citations = append(citations, cur)
	}
	top := citations[size-1]

	var sink int64
	for q := int64(0); q < queries; q++ {
		state = (state*1103515245 + 12345) & 2147483647
		n := 1 + (state/256)%size
		sink = (sink*131 + hIndexPrefix(citations, n)) % 1000000007
	}

	fmt.Println(sink)
	fmt.Printf("size %d queries %d top %d\n", size, queries, top)
}
