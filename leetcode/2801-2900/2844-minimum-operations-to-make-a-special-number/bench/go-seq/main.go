// LeetCode #2844: Minimum Operations to Make a Special Number -- the
// bench, mirrored from special.kara: one pass from the right, ending
// the number at the first 0 or 5 after a 0, or 2 or 7 after a 5.
package main

import "fmt"

func minimumOperations(num string) int64 {
	n := int64(len(num))
	zero, five := false, false
	for i := n - 1; i >= 0; i-- {
		d := num[i]
		if (zero && (d == '0' || d == '5')) || (five && (d == '2' || d == '7')) {
			return n - i - 2
		}
		if d == '0' {
			zero = true
		}
		if d == '5' {
			five = true
		}
	}
	if zero {
		return n - 1
	}
	return n
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 100000, 300
	seed := int64(2844)
	numbers := make([]string, 0, count)
	for c := 0; c < count; c++ {
		n := nextRandom(&seed)%100 + 1
		digits := make([]byte, 0, n)
		for i := int64(0); i < n; i++ {
			low := int64(0)
			if i == 0 && n > 1 {
				low = 1
			}
			digits = append(digits, byte(48+low+nextRandom(&seed)%(10-low)))
		}
		numbers = append(numbers, string(digits))
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, num := range numbers {
			ops := minimumOperations(num)
			total += ops
			check = (check*31 + ops + r) % 1000000007
		}
	}
	fmt.Printf("%d numbers, %d rounds: %d operations, checksum %d\n", count, rounds, total, check)
}
