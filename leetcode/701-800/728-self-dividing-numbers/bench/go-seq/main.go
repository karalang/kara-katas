// LeetCode #728: Self Dividing Numbers -- each digit, by remainders.
// Benchmark mirror of the Kara star arm: peel each number's digits off
// with % 10 and / 10, stopping at a 0 or a digit that does not divide
// it, and collect the numbers that pass.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func selfDividing(n int64) bool {
	for rest := n; rest > 0; rest /= 10 {
		d := rest % 10
		if d == 0 || n%d != 0 {
			return false
		}
	}
	return true
}

func selfDividingNumbers(left, right int64) []int64 {
	var out []int64
	for n := left; n <= right; n++ {
		if selfDividing(n) {
			out = append(out, n)
		}
	}
	return out
}

func main() {
	seed := int64(728)
	var count, sum int64
	for r := 0; r < 40000; r++ {
		a := 1 + nextRandom(&seed)%10000
		b := 1 + nextRandom(&seed)%10000
		left, right := a, b
		if b < a {
			left, right = b, a
		}
		found := selfDividingNumbers(left, right)
		count += int64(len(found))
		for _, n := range found {
			sum += n
		}
	}
	fmt.Printf("40000 random ranges: %d numbers, sum %d\n", count, sum)
}
