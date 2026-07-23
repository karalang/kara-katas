package main

import "fmt"

// ASCII: '+'=43 '-'=45 '('=40 ')'=41 '0'=48 '9'=57
func calculate(bytes []int64, n int64) int64 {
	var result int64 = 0
	var sign int64 = 1
	stack := make([]int64, 0, 64)
	i := int64(0)
	for i < n {
		b := bytes[i]
		if b >= 48 && b <= 57 {
			var num int64 = 0
			for i < n && bytes[i] >= 48 && bytes[i] <= 57 {
				num = num*10 + (bytes[i] - 48)
				i++
			}
			result = result + sign*num
		} else if b == 43 {
			sign = 1
			i++
		} else if b == 45 {
			sign = -1
			i++
		} else if b == 40 {
			stack = append(stack, result)
			stack = append(stack, sign)
			result = 0
			sign = 1
			i++
		} else if b == 41 {
			var savedSign int64 = 1
			if len(stack) > 0 {
				savedSign = stack[len(stack)-1]
				stack = stack[:len(stack)-1]
			}
			var savedResult int64 = 0
			if len(stack) > 0 {
				savedResult = stack[len(stack)-1]
				stack = stack[:len(stack)-1]
			}
			result = savedResult + savedSign*result
			i++
		} else {
			i++
		}
	}
	return result
}

func pushNumber(buf *[]int64, num int64) {
	if num >= 100 {
		*buf = append(*buf, 48+num/100)
		*buf = append(*buf, 48+(num/10)%10)
		*buf = append(*buf, 48+num%10)
	} else if num >= 10 {
		*buf = append(*buf, 48+num/10)
		*buf = append(*buf, 48+num%10)
	} else {
		*buf = append(*buf, 48+num)
	}
}

func main() {
	var nums int64 = 250000
	var passes int64 = 80
	var maxDepth int64 = 16
	var modulus int64 = 1000000007

	buf := make([]int64, 0, nums*6+64)
	var state int64 = 12345
	var depth int64 = 0

	state = (state*1103515245 + 12345) & 2147483647
	pushNumber(&buf, state%1000)

	for t := int64(1); t < nums; t++ {
		state = (state*1103515245 + 12345) & 2147483647
		if state%2 == 0 {
			buf = append(buf, 43)
		} else {
			buf = append(buf, 45)
		}

		state = (state*1103515245 + 12345) & 2147483647
		opens := state % 3
		openedHere := false
		for o := int64(0); o < opens; o++ {
			if depth < maxDepth {
				buf = append(buf, 40)
				depth++
				openedHere = true
			}
		}

		if openedHere {
			state = (state*1103515245 + 12345) & 2147483647
			if state%4 == 0 {
				buf = append(buf, 45)
			}
		}

		state = (state*1103515245 + 12345) & 2147483647
		pushNumber(&buf, state%1000)

		state = (state*1103515245 + 12345) & 2147483647
		closes := state % 3
		for c := int64(0); c < closes; c++ {
			if depth > 0 {
				buf = append(buf, 41)
				depth--
			}
		}
	}
	for depth > 0 {
		buf = append(buf, 41)
		depth--
	}

	n := int64(len(buf))
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		buf[0] = 48 + (p % 10)
		r := calculate(buf, n)
		sink = ((sink+r)%modulus + modulus) % modulus
	}
	fmt.Println(sink)
}
