// Benchmark workload for LeetCode #256 — Paint House (Go mirror).
// Mirrors paint_house.kara algorithm-for-algorithm.
package main

import "fmt"

type Cost struct{ a, b, c int64 }

func min2(x, y int64) int64 {
	if x < y {
		return x
	}
	return y
}

func main() {
	var n int64 = 150000
	var rounds int64 = 800

	cost := make([]Cost, n)
	var state int64 = 256256
	var cheap, runLeft int64
	for i := int64(0); i < n; i++ {
		if runLeft == 0 {
			state = (state*1103515245 + 12345) & 2147483647
			runLeft = (state/65536)%9 + 2
			state = (state*1103515245 + 12345) & 2147483647
			cheap = (state / 65536) % 3
		}
		state = (state*1103515245 + 12345) & 2147483647
		lo := (state/65536)%10 + 1
		state = (state*1103515245 + 12345) & 2147483647
		m1 := (state/65536)%40 + 40
		state = (state*1103515245 + 12345) & 2147483647
		m2 := (state/65536)%40 + 40
		switch cheap {
		case 0:
			cost[i] = Cost{lo, m1, m2}
		case 1:
			cost[i] = Cost{m1, lo, m2}
		default:
			cost[i] = Cost{m1, m2, lo}
		}
		runLeft--
	}

	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		a, b, c := cost[0].a, cost[0].b, cost[0].c
		for k := int64(1); k < n; k++ {
			na := cost[k].a + min2(b, c)
			nb := cost[k].b + min2(a, c)
			nc := cost[k].c + min2(a, b)
			a, b, c = na, nb, nc
		}
		sink = (sink*31 + min2(a, min2(b, c))) % 1000000007
	}
	fmt.Println(sink)
}
