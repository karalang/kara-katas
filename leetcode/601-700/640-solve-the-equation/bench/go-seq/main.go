// Benchmark for #640: mirror of solve_the_equation.kara (the ★ arm: each
// side read once into a count of x and a constant) on the same workload.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

const rounds = 200000

func side(text string) (int64, int64) {
	var xs, constant int64
	i := 0
	n := len(text)
	for i < n {
		var sign int64 = 1
		if text[i] == '+' || text[i] == '-' {
			if text[i] == '-' {
				sign = -1
			}
			i++
		}
		var value int64
		digits := 0
		for i < n && text[i] >= '0' && text[i] <= '9' {
			value = value*10 + int64(text[i]-'0')
			digits++
			i++
		}
		if i < n && text[i] == 'x' {
			if digits == 0 {
				xs += sign
			} else {
				xs += sign * value
			}
			i++
		} else {
			constant += sign * value
		}
	}
	return xs, constant
}

func solveEquation(equation string) string {
	eq := 0
	for equation[eq] != '=' {
		eq++
	}
	a, b := side(equation[:eq])
	c, d := side(equation[eq+1:])
	if a == c {
		if b == d {
			return "Infinite solutions"
		}
		return "No solution"
	}
	return "x=" + strconv.FormatInt((d-b)/(a-c), 10)
}

var seed int64 = 640

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomSide(terms int) (string, int64, int64) {
	var text strings.Builder
	var xs, constant int64
	for t := 0; t < terms; t++ {
		minus := nextRandom()%2 == 0
		if minus {
			text.WriteByte('-')
		} else if t > 0 {
			text.WriteByte('+')
		}
		var sign int64 = 1
		if minus {
			sign = -1
		}
		value := nextRandom() % 100
		if nextRandom()%2 == 0 {
			fmt.Fprintf(&text, "%dx", value)
			xs += sign * value
		} else {
			fmt.Fprintf(&text, "%d", value)
			constant += sign * value
		}
	}
	return text.String(), xs, constant
}

func main() {
	var equations []string
	for e := 0; e < 20; e++ {
		left, a, b := randomSide(125)
		right, c, d := randomSide(125)
		text := left + "=" + right
		if a != c {
			rem := (d - b) % (a - c)
			if rem > 0 {
				text = fmt.Sprintf("%s-%d", text, rem)
			} else if rem < 0 {
				text = fmt.Sprintf("%s+%d", text, -rem)
			}
		}
		equations = append(equations, text)
	}
	var solved, sum int64
	for round := 0; round < rounds; round++ {
		answer := solveEquation(equations[round%20])
		if strings.HasPrefix(answer, "x=") {
			solved++
			v, _ := strconv.ParseInt(answer[2:], 10, 64)
			sum += v
		}
	}
	fmt.Printf("20 equations, %d rounds: %d solved, x adding to %d\n", rounds, solved, sum)
}
