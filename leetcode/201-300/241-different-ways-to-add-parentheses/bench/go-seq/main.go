// Benchmark harness for LeetCode #241 — Different Ways to Add Parentheses.
// Mirrors different_ways.kara algorithm-for-algorithm, including the
// deliberately unmemoized recursion.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func tokenize(expr string) []int64 {
	tok := make([]int64, 0, 32)
	i := 0
	n := len(expr)
	for i < n {
		b := int64(expr[i])
		if b == 43 || b == 45 || b == 42 {
			tok = append(tok, b)
			i++
		} else {
			var v int64
			for i < n {
				d := int64(expr[i])
				if d >= 48 && d <= 57 {
					v = v*10 + (d - 48)
					i++
				} else {
					break
				}
			}
			tok = append(tok, v)
		}
	}
	return tok
}

func ways(tok []int64, lo int64, hi int64) []int64 {
	res := make([]int64, 0, 8)
	if lo == hi {
		return append(res, tok[lo])
	}
	for k := lo + 1; k < hi; k += 2 {
		op := tok[k]
		left := ways(tok, lo, k-1)
		right := ways(tok, k+1, hi)
		for _, l := range left {
			for _, r := range right {
				switch op {
				case 43:
					res = append(res, l+r)
				case 45:
					res = append(res, l-r)
				default:
					res = append(res, l*r)
				}
			}
		}
	}
	return res
}

const (
	NP    = 6
	NOPS  = 11
	Iters = 30
)

func main() {
	ops := []string{"+", "-", "*"}

	toks := make([][]int64, NP)
	for j := 0; j < NP; j++ {
		var e strings.Builder
		for t := 0; t <= NOPS; t++ {
			e.WriteString(strconv.Itoa((t % 9) + 1))
			if t < NOPS {
				e.WriteString(ops[(t+j)%3])
			}
		}
		toks[j] = tokenize(e.String())
	}

	var sink int64
	for it := 0; it < Iters; it++ {
		idx := (it * 5) % NP
		tk := toks[idx]
		for _, v := range ways(tk, 0, int64(len(tk))-1) {
			sink += v
		}
	}
	fmt.Println(sink)
}
