// LeetCode #2232: Minimize Result by Adding Parentheses to Expression --
// the benchmark's Go mirror of parentheses.kara: every place for the two
// parentheses, the first smallest a * (b + c) * d kept.
package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func parse(s string) int64 {
	v, _ := strconv.ParseInt(s, 10, 64)
	return v
}

func minimizeResult(expression string) string {
	plus := strings.Index(expression, "+")
	left, right := expression[:plus], expression[plus+1:]
	var best int64 = math.MaxInt64
	answer := ""
	for i := 0; i < len(left); i++ {
		for j := 1; j <= len(right); j++ {
			var a, d int64 = 1, 1
			if i > 0 {
				a = parse(left[:i])
			}
			b := parse(left[i:])
			c := parse(right[:j])
			if j < len(right) {
				d = parse(right[j:])
			}
			value := a * (b + c) * d
			if value < best {
				best = value
				answer = fmt.Sprintf("%s(%s+%s)%s", left[:i], left[i:], right[:j], right[j:])
			}
		}
	}
	return answer
}

var seed int64 = 2232

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func drawExpression() string {
	left := nextRandom()%8 + 1
	right := nextRandom()%(9-left) + 1
	b := make([]byte, 0, left+right+1)
	for k := int64(0); k < left+right+1; k++ {
		if k == left {
			b = append(b, '+')
		} else {
			b = append(b, byte(49+nextRandom()%9))
		}
	}
	return string(b)
}

func main() {
	expressions := make([]string, 20000)
	for i := range expressions {
		expressions[i] = drawExpression()
	}
	var check int64
	for r := 0; r < 20; r++ {
		// punch: one expression drawn again before each pass over all
		at := nextRandom() % 20000
		expressions[at] = drawExpression()
		for _, expression := range expressions {
			answer := minimizeResult(expression)
			check = (check*31 + int64(len(answer)) + int64(strings.Index(answer, "("))*11 + int64(strings.Index(answer, ")"))) % 1000000007
		}
	}
	fmt.Printf("20 passes over 20000 expressions: checksum %d\n", check)
}
