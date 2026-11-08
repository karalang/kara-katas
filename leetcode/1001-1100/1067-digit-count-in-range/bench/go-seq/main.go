// LeetCode #1067: Digit Count in Range -- the benchmark's Go mirror of
// digit_count.kara: the same place by place count over a million queries.
package main

import "fmt"

func countTo(d, n int64) int64 {
	var total int64
	var p int64 = 1
	for p <= n {
		above := n / (p * 10)
		digit := n / p % 10
		below := n % p
		if d == 0 {
			if above == 0 {
				break
			}
			total += (above - 1) * p
		} else {
			total += above * p
		}
		if digit > d {
			total += p
		} else if digit == d {
			total += below + 1
		}
		p *= 10
	}
	return total
}

func digitsCount(d, low, high int64) int64 {
	return countTo(d, high) - countTo(d, low-1)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var seed int64 = 1067
	queries := make([][3]int64, 0)
	for i := 0; i < 1000000; i++ {
		d := nextRandom(&seed) % 10
		a := (nextRandom(&seed)*32768+nextRandom(&seed))%200000000 + 1
		b := (nextRandom(&seed)*32768+nextRandom(&seed))%200000000 + 1
		queries = append(queries, [3]int64{d, min(a, b), max(a, b)})
	}
	var calls, total, check int64
	for _, q := range queries {
		answer := digitsCount(q[0], q[1], q[2])
		total += answer
		check = (check*31 + answer) % 1000000007
		calls++
	}
	fmt.Printf("%d calls: answers sum %d, checksum %d\n", calls, total, check)
}
