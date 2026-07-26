// Benchmark harness for LeetCode #134 — Gas Station.
// Mirrors gas_station.kara algorithm-for-algorithm.
package main

import "fmt"

func canComplete(gas []int64, cost []int64) int64 {
	n := len(gas)
	var total, tank, start int64
	for i := 0; i < n; i++ {
		d := gas[i] - cost[i]
		total += d
		tank += d
		if tank < 0 {
			start = int64(i) + 1
			tank = 0
		}
	}
	if total >= 0 {
		return start
	}
	return -1
}

func lcg(seed int64, n int64, cap int64) []int64 {
	out := make([]int64, 0, n)
	x := seed
	for k := int64(0); k < n; k++ {
		x = (x*1103515245 + 12345) % 2147483648
		out = append(out, (x/65536)%cap)
	}
	return out
}

const (
	NP    = 8
	N     = 200000
	Iters = 1200
)

func main() {
	gases := make([][]int64, NP)
	costs := make([][]int64, NP)
	for j := int64(0); j < NP; j++ {
		gases[j] = lcg(j+1, N, 100)
		if j%2 == 0 {
			costs[j] = lcg(j+100, N, 90)
		} else {
			costs[j] = lcg(j+100, N, 110)
		}
	}

	var sink int64
	for it := int64(0); it < Iters; it++ {
		idx := (it * 3) % NP
		sink = (sink + canComplete(gases[idx], costs[idx])) % 1000000007
	}
	fmt.Println(sink)
}
