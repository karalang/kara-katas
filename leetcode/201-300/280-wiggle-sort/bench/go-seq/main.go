// LeetCode 280 bench mirror — Go. Same greedy, refresh and sink.
package main

import "fmt"

const N = 2000000
const Rounds = 30

func wiggleSort(a []int64) {
	for i := 1; i < len(a); i++ {
		if i%2 == 1 {
			if a[i] < a[i-1] {
				a[i], a[i-1] = a[i-1], a[i]
			}
		} else {
			if a[i] > a[i-1] {
				a[i], a[i-1] = a[i-1], a[i]
			}
		}
	}
}

func main() {
	src := make([]int64, N)
	seed := int64(20260818)
	for i := 0; i < N; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		src[i] = seed % 1000003
	}
	work := make([]int64, N)
	var sink int64
	for r := 0; r < Rounds; r++ {
		copy(work, src)
		wiggleSort(work)
		var h int64
		for j := 0; j < N; j++ {
			h = (h*31 + work[j]) % 1000000007
		}
		sink = (sink + h) % 1000000007
	}
	fmt.Println(sink)
}
