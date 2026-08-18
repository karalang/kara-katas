// LeetCode 283 bench mirror — Go. Same cursor, refresh and sink.
package main

import "fmt"

const N = 2000000
const Rounds = 60

func moveZeroes(a []int64, stores *int64) {
	write := 0
	for i := 0; i < len(a); i++ {
		if a[i] != 0 {
			a[write] = a[i]
			*stores++
			write++
		}
	}
	for write < len(a) {
		a[write] = 0
		*stores++
		write++
	}
}

func main() {
	seed := int64(20260821)
	src := make([]int64, N)
	for i := 0; i < N; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		if seed%2 == 0 {
			src[i] = 0
		} else {
			src[i] = seed % 100003
		}
	}
	work := make([]int64, N)
	var sink, total int64
	for r := 0; r < Rounds; r++ {
		copy(work, src)
		var st int64
		moveZeroes(work, &st)
		total += st
		var h int64
		for j := 0; j < N; j++ {
			h = (h*31 + work[j]) % 1000000007
		}
		sink = (sink + h) % 1000000007
	}
	fmt.Println(sink, total)
}
