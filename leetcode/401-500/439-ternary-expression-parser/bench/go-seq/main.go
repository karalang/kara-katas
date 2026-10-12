// Benchmark for #439: mirror of parse_ternary.kara (a stack, scanning
// from the right) on 200 random expressions of 2,499 ternaries each,
// built once and evaluated 20 times over.
package main

import (
	"fmt"
	"strings"
)

func parseTernary(expression string) byte {
	e := []byte(expression)
	stack := []byte{}
	i := len(e)
	for i > 0 {
		i--
		if len(stack) > 0 && stack[len(stack)-1] == '?' {
			yes := stack[len(stack)-2]
			no := stack[len(stack)-4]
			stack = stack[:len(stack)-4]
			if e[i] == 'T' {
				stack = append(stack, yes)
			} else {
				stack = append(stack, no)
			}
		} else {
			stack = append(stack, e[i])
		}
	}
	return stack[0]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

// Appends a random expression of exactly n ternaries to out: a random
// split of the n - 1 below the root between its two branches.
func randomExpression(seed *int64, n int64, out *strings.Builder) {
	if n == 0 {
		r := nextRandom(seed) % 12
		if r < 10 {
			out.WriteByte(byte('0' + r))
		} else if r == 10 {
			out.WriteByte('T')
		} else {
			out.WriteByte('F')
		}
		return
	}
	if nextRandom(seed)%2 == 0 {
		out.WriteByte('T')
	} else {
		out.WriteByte('F')
	}
	out.WriteByte('?')
	left := nextRandom(seed) % n
	randomExpression(seed, left, out)
	out.WriteByte(':')
	randomExpression(seed, n-1-left, out)
}

func main() {
	const count, ternaries, rounds = 200, 2499, 20
	seed := int64(439)
	expressions := []string{}
	for k := 0; k < count; k++ {
		var b strings.Builder
		randomExpression(&seed, ternaries, &b)
		expressions = append(expressions, b.String())
	}
	digits := 0
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		for _, e := range expressions {
			value := parseTernary(e)
			if value != 'T' && value != 'F' {
				digits++
			}
			checksum = (checksum*31 + int64(value) + round) % 1000000007
		}
	}
	fmt.Printf("%d expressions of %d characters, %d rounds: %d digits, checksum %d\n", count, len(expressions[0]), rounds, digits, checksum)
}
