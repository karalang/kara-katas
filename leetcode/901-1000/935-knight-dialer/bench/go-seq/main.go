// LeetCode #935: Knight Dialer -- bench: counts by last digit, one jump
// at a time. Mirrors knight_dialer.kara, .c, .rs and .py.

package main

import "fmt"

var jumps = [][]int{{4, 6}, {6, 8}, {7, 9}, {4, 8}, {0, 3, 9}, {}, {0, 1, 7}, {2, 6}, {1, 3}, {2, 4}}

func knightDialer(n int64) int64 {
	const modulus int64 = 1000000007
	counts := make([]int64, 10)
	for d := range counts {
		counts[d] = 1
	}
	for step := int64(1); step < n; step++ {
		next := make([]int64, 10)
		for d := 0; d < 10; d++ {
			for _, from := range jumps[d] {
				next[d] = (next[d] + counts[from]) % modulus
			}
		}
		counts = next
	}
	var total int64
	for _, c := range counts {
		total = (total + c) % modulus
	}
	return total
}

func main() {
	var rounds int64 = 20
	var low int64 = 4901
	var high int64 = 5000
	var total int64
	var check int64
	for r := int64(0); r < rounds; r++ {
		// each round counts every length from low to high, starting from
		// a different one
		for i := int64(0); i < high-low+1; i++ {
			n := low + (r+i)%(high-low+1)
			a := knightDialer(n)
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over n from %d to %d: answers summing to %d, checksum %d\n", rounds, low, high, total, check)
}
