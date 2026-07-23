package main

import "fmt"

func evalRPN(tok []int64, stk []int64, modp int64) int64 {
	t := len(tok)
	sp := 0
	for i := 0; i < t; i++ {
		x := tok[i]
		if x >= 0 {
			stk[sp] = x
			sp++
		} else {
			op := -x - 1
			sp--
			b := stk[sp]
			sp--
			a := stk[sp]
			var r int64
			if op == 0 {
				r = a + b
			} else if op == 1 {
				r = a - b
			} else if op == 2 {
				r = a * b
			} else {
				r = a / b
			}
			r = ((r % modp) + modp) % modp
			stk[sp] = r
			sp++
		}
	}
	return stk[0]
}

func main() {
	var m, punches, modp, opr int64 = 100000, 700, 1000000007, 1000

	tok := make([]int64, 0, 2*m+1)
	var state int64 = 12345

	state = (state*1103515245 + 12345) & 2147483647
	tok = append(tok, state%opr+1)
	state = (state*1103515245 + 12345) & 2147483647
	tok = append(tok, state%opr+1)
	state = (state*1103515245 + 12345) & 2147483647
	tok = append(tok, -(state%4)-1)

	for k := int64(2); k <= m; k++ {
		state = (state*1103515245 + 12345) & 2147483647
		tok = append(tok, state%opr+1)
		state = (state*1103515245 + 12345) & 2147483647
		tok = append(tok, -(state%4)-1)
	}

	stk := make([]int64, 4)

	var sink int64 = 0
	for pn := int64(0); pn < punches; pn++ {
		state = (state*1103515245 + 12345) & 2147483647
		r := state % (m + 1)
		var tokpos int64
		if r == 0 {
			tokpos = 0
		} else {
			tokpos = 2*r - 1
		}
		state = (state*1103515245 + 12345) & 2147483647
		tok[tokpos] = state%opr + 1
		res := evalRPN(tok, stk, modp)
		sink = (sink + res) % modp
	}
	fmt.Println(sink)
}
