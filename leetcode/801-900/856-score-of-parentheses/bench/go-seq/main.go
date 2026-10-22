// Benchmark for #856: Score of Parentheses -- the ★ arm, mirroring
// score_of_parentheses.kara.
package main

import "fmt"

func scoreOfParentheses(s string) int64 {
	stack := []int64{0}
	for _, c := range s {
		if c == '(' {
			stack = append(stack, 0)
		} else {
			inner := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			worth := int64(1)
			if inner != 0 {
				worth = 2 * inner
			}
			stack[len(stack)-1] += worth
		}
	}
	return stack[0]
}

var seed int64 = 856

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 64, 4000000
	strings := []string{}
	for g := 0; g < count; g++ {
		s := []byte{}
		opens, balance := 0, 0
		for len(s) < 50 {
			if opens < 25 && (balance == 0 || nextRandom()%4 < int64(1+g%3)) {
				s = append(s, '(')
				opens++
				balance++
			} else {
				s = append(s, ')')
				balance--
			}
		}
		strings = append(strings, string(s))
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		k := scoreOfParentheses(strings[round%count])
		total += k
		checksum = (checksum*31 + k) % 1000000007
	}
	fmt.Printf("%d rounds of 64 strings: scores sum to %d, checksum %d\n", rounds, total, checksum)
}
