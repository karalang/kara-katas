// LeetCode #1106: Parsing A Boolean Expression -- the bench in Go: the ★
// arm (recursive descent from a shared position) over 32 expressions of
// up to about 2 * 10^4 characters, each round flipping one value in every
// expression and parsing it again.
package main

import "fmt"

func parse(s []rune, at *int) bool {
	c := s[*at]
	*at++
	switch c {
	case 't':
		return true
	case 'f':
		return false
	}
	*at++
	var values []bool
	for {
		values = append(values, parse(s, at))
		next := s[*at]
		*at++
		if next == ')' {
			break
		}
	}
	switch c {
	case '!':
		return !values[0]
	case '&':
		for _, v := range values {
			if !v {
				return false
			}
		}
		return true
	default:
		for _, v := range values {
			if v {
				return true
			}
		}
		return false
	}
}

var seed int64 = 1106

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomExpr(out *[]rune, budget, depth int64) {
	if budget <= 1 || depth == 0 {
		if nextRandom()%2 == 0 {
			*out = append(*out, 't')
		} else {
			*out = append(*out, 'f')
		}
		return
	}
	op := nextRandom() % 3
	if op == 0 {
		*out = append(*out, '!', '(')
		randomExpr(out, budget-1, depth-1)
		*out = append(*out, ')')
		return
	}
	k := nextRandom()%4 + 1
	if op == 1 {
		*out = append(*out, '&', '(')
	} else {
		*out = append(*out, '|', '(')
	}
	for i := int64(0); i < k; i++ {
		if i > 0 {
			*out = append(*out, ',')
		}
		randomExpr(out, (budget-1)/k, depth-1)
	}
	*out = append(*out, ')')
}

func main() {
	var cases [][]rune
	var values [][]int
	length := 0
	for c := 0; c < 32; c++ {
		var e []rune
		randomExpr(&e, 6000, 20)
		var at []int
		for i, ch := range e {
			if ch == 't' || ch == 'f' {
				at = append(at, i)
			}
		}
		length += len(e)
		cases = append(cases, e)
		values = append(values, at)
	}
	trues := 0
	var check int64
	for round := 0; round < 200; round++ {
		for j := range cases {
			i := values[j][(round*7919+j*104729)%len(values[j])]
			if cases[j][i] == 't' {
				cases[j][i] = 'f'
			} else {
				cases[j][i] = 't'
			}
			at := 0
			v := parse(cases[j], &at)
			if v {
				trues++
			}
			if v {
				check = (check*31 + 2) % 1000000007
			} else {
				check = (check*31 + 1) % 1000000007
			}
		}
	}
	fmt.Printf("200 rounds over 32 expressions of %d characters: %d true, checksum %d\n", length, trues, check)
}
