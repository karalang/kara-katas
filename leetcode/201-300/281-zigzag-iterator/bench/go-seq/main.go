// LeetCode 281 bench mirror — Go. Same cursor iterator, same skip scan.
package main

import "fmt"

const K = 64
const Rounds = 2200

func drainSink(lists [][]int64) int64 {
	var cursor [K]int
	var remaining int64
	for i := 0; i < K; i++ {
		remaining += int64(len(lists[i]))
	}
	turn, tried := 0, 0
	for tried < K && cursor[turn] >= len(lists[turn]) {
		turn = (turn + 1) % K
		tried++
	}
	var h, pos int64 = 0, 1
	for remaining > 0 {
		t := turn
		v := lists[t][cursor[t]]
		cursor[t]++
		remaining--
		h = (h*31 + v*pos) % 1000000007
		pos++
		turn = (t + 1) % K
		scan := 0
		for scan < K && cursor[turn] >= len(lists[turn]) {
			turn = (turn + 1) % K
			scan++
		}
	}
	return h
}

func main() {
	seed := int64(20260819)
	lists := make([][]int64, K)
	for i := 0; i < K; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		ln := 1 + (seed/7)%2000
		v := make([]int64, ln)
		for j := int64(0); j < ln; j++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			v[j] = seed % 100003
		}
		lists[i] = v
	}
	var sink int64
	for r := 0; r < Rounds; r++ {
		sink = (sink + drainSink(lists)) % 1000000007
	}
	fmt.Println(sink)
}
