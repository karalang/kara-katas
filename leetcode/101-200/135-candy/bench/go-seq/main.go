// Benchmark harness for LeetCode #135 — Candy.
// Mirrors candy.kara algorithm-for-algorithm, including the explicit
// descending index loop for the right-to-left pass.
package main

import "fmt"

func candy(ratings []int64) int64 {
	n := int64(len(ratings))
	if n == 0 {
		return 0
	}
	c := make([]int64, n)
	for k := int64(0); k < n; k++ {
		c[k] = 1
	}

	for i := int64(1); i < n; i++ {
		if ratings[i] > ratings[i-1] {
			c[i] = c[i-1] + 1
		}
	}

	for i := n - 2; i >= 0; i-- {
		if ratings[i] > ratings[i+1] && c[i] <= c[i+1] {
			c[i] = c[i+1] + 1
		}
	}

	var total int64
	for i := int64(0); i < n; i++ {
		total += c[i]
	}
	return total
}

func lcg(seed int64, n int64, cap int64) []int64 {
	out := make([]int64, 0, n)
	x := seed
	for k := int64(0); k < n; k++ {
		x = (x*1103515245 + 12345) % 2147483648
		wd0 := x / 65536
		x = (x*1103515245 + 12345) % 2147483648
		out = append(out, (wd0*32768+x/65536)%cap)
	}
	return out
}

const (
	NP    = 8
	N     = 200000
	Iters = 150
)

func main() {
	arrays := make([][]int64, NP)
	for j := int64(0); j < NP; j++ {
		if j%2 == 0 {
			arrays[j] = lcg(j+1, N, 4)
		} else {
			arrays[j] = lcg(j+1, N, 100000)
		}
	}

	var sink int64
	for it := int64(0); it < Iters; it++ {
		idx := (it * 3) % NP
		sink = (sink + candy(arrays[idx])) % 1000000007
	}
	fmt.Println(sink)
}
