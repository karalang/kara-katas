// LeetCode #12 — Go seq bench peer for bench/greedy.kara. Same greedy
// matcher, same workload (K=10M LCG-driven inputs in [1,3999]), same
// sink as the Kara / Rust / C mirrors.

package main

import "fmt"

func intToRoman(num int64) []int32 {
	out := make([]int32, 0, 15)
	n := num
	for n >= 1000 {
		out = append(out, 'M')
		n -= 1000
	}
	if n >= 900 {
		out = append(out, 'C', 'M')
		n -= 900
	}
	if n >= 500 {
		out = append(out, 'D')
		n -= 500
	}
	if n >= 400 {
		out = append(out, 'C', 'D')
		n -= 400
	}
	for n >= 100 {
		out = append(out, 'C')
		n -= 100
	}
	if n >= 90 {
		out = append(out, 'X', 'C')
		n -= 90
	}
	if n >= 50 {
		out = append(out, 'L')
		n -= 50
	}
	if n >= 40 {
		out = append(out, 'X', 'L')
		n -= 40
	}
	for n >= 10 {
		out = append(out, 'X')
		n -= 10
	}
	if n >= 9 {
		out = append(out, 'I', 'X')
		n -= 9
	}
	if n >= 5 {
		out = append(out, 'V')
		n -= 5
	}
	if n >= 4 {
		out = append(out, 'I', 'V')
		n -= 4
	}
	for n >= 1 {
		out = append(out, 'I')
		n -= 1
	}
	return out
}

func scoreRoman(r []int32) int64 {
	var s int64 = 0
	for _, c := range r {
		s += int64(c)
	}
	return s
}

func main() {
	const kIters int64 = 10_000_000
	var sum int64 = 0
	for k := int64(0); k < kIters; k++ {
		raw := k*2654435769 + 305419896
		num := (raw%3999+3999)%3999 + 1
		r := intToRoman(num)
		sum += scoreRoman(r)
	}
	fmt.Println(sum)
}
