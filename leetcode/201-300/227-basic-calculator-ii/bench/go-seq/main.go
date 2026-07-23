package main

import "fmt"

// ASCII: '+'=43 '-'=45 '*'=42 '/'=47 '0'=48 '9'=57
func calculate(bytes []int64, n int64) int64 {
	stack := make([]int64, 0, n+1)
	var num int64 = 0
	var op int64 = 43 // '+'
	for i := int64(0); i < n; i++ {
		b := bytes[i]
		if b >= 48 && b <= 57 {
			num = num*10 + (b - 48)
		}
		isOp := b == 43 || b == 45 || b == 42 || b == 47
		if isOp || i == n-1 {
			if op == 43 {
				stack = append(stack, num)
			} else if op == 45 {
				stack = append(stack, -num)
			} else if op == 42 {
				var t int64 = 0
				if len(stack) > 0 {
					t = stack[len(stack)-1]
					stack = stack[:len(stack)-1]
				}
				stack = append(stack, t*num)
			} else { // '/'
				var t int64 = 0
				if len(stack) > 0 {
					t = stack[len(stack)-1]
					stack = stack[:len(stack)-1]
				}
				stack = append(stack, t/num) // truncates toward zero
			}
			op = b
			num = 0
		}
	}
	var total int64 = 0
	for _, v := range stack {
		total += v
	}
	return total
}

func pushNumber(buf *[]int64, num int64) {
	if num >= 10 {
		*buf = append(*buf, 48+num/10)
		*buf = append(*buf, 48+num%10)
	} else {
		*buf = append(*buf, 48+num)
	}
}

func main() {
	var tokens int64 = 200000
	var passes int64 = 250
	var modulus int64 = 1000000007

	buf := make([]int64, 0, tokens*3+8)
	var state int64 = 12345

	state = (state*1103515245 + 12345) & 2147483647
	pushNumber(&buf, (state%99)+1)

	prevHigh := false
	for t := int64(1); t < tokens; t++ {
		state = (state*1103515245 + 12345) & 2147483647
		var opsel int64
		if prevHigh {
			opsel = state % 2
		} else {
			opsel = state % 4
		}
		if opsel == 0 {
			buf = append(buf, 43)
			prevHigh = false
		} else if opsel == 1 {
			buf = append(buf, 45)
			prevHigh = false
		} else if opsel == 2 {
			buf = append(buf, 42)
			prevHigh = true
		} else {
			buf = append(buf, 47)
			prevHigh = true
		}
		state = (state*1103515245 + 12345) & 2147483647
		pushNumber(&buf, (state%99)+1)
	}

	n := int64(len(buf))
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		buf[0] = 49 + (p % 9)
		r := calculate(buf, n)
		sink = ((sink+r)%modulus + modulus) % modulus
	}
	fmt.Println(sink)
}
