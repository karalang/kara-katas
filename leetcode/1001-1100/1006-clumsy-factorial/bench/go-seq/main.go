// Benchmark: LeetCode #1006 Clumsy Factorial -- the ★ arm, a stack, on
// every n up to 10000, LeetCode's largest.
// Mirrors clumsy.kara, .c, .rs and .py.
package main

import "fmt"

func clumsy(n int64) int64 {
	stack := []int64{n}
	op := 0
	for x := n - 1; x > 0; x-- {
		last := len(stack) - 1
		switch op {
		case 0:
			stack[last] *= x
		case 1:
			stack[last] /= x
		case 2:
			stack = append(stack, x)
		default:
			stack = append(stack, -x)
		}
		op = (op + 1) % 4
	}
	sum := int64(0)
	for _, t := range stack {
		sum += t
	}
	return sum
}

func main() {
	rounds := int64(4)
	total := int64(0)
	check := int64(0)
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 10000; i++ {
			n := i + 1
			if r%2 == 1 {
				n = 10000 - i
			}
			got := clumsy(n)
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d rounds over every n up to 10000: answers sum to %d, checksum %d\n", rounds, total, check)
}
