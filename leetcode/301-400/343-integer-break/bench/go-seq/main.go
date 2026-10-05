// Benchmark workload for LeetCode #343 — Go mirror of integer_break.kara.
package main

import "fmt"

const (
	LEN     = 20000
	PUNCHES = 20
	MODULUS = 1073741789
)

func integerBreak(n int64) int64 {
	best := make([]int64, n+1)
	for i := int64(2); i <= n; i++ {
		for j := int64(1); j < i; j++ {
			whole := j * (i - j)
			broken := j * best[i-j]
			if whole > best[i] {
				best[i] = whole
			}
			if broken > best[i] {
				best[i] = broken
			}
		}
	}
	return best[n]
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var seed int64 = 343
	a := make([]int64, 0)
	for i := 0; i < LEN; i++ {
		a = append(a, 2+next(&seed)%57)
	}
	var sink int64
	for p := 0; p < PUNCHES; p++ {
		pos := (next(&seed)*32768 + next(&seed)) % LEN
		a[pos] = 2 + next(&seed)%57
		var sum int64
		for _, n := range a {
			sum = (sum + integerBreak(n)) % MODULUS
		}
		sink = (sink*31 + sum) % MODULUS
	}
	fmt.Printf("sink %d\n", sink)
}
