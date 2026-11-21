// LeetCode #2478: Number of Beautiful Partitions -- bench, Go mirror of
// beauty.kara.
package main

import "fmt"

const mod = 1000000007

func isPrimeDigit(c int64) bool { return c == 2 || c == 3 || c == 5 || c == 7 }

func beautifulPartitions(digits []int64, k, minLength int64) int64 {
	n := int64(len(digits))
	if !isPrimeDigit(digits[0]) || isPrimeDigit(digits[n-1]) {
		return 0
	}
	cut := make([]bool, n+1)
	for i := int64(0); i <= n; i++ {
		cut[i] = i == n || (i > 0 && !isPrimeDigit(digits[i-1]) && isPrimeDigit(digits[i]))
	}
	ways := make([]int64, n+1)
	ways[0] = 1
	for r := int64(0); r < k; r++ {
		next := make([]int64, n+1)
		running := int64(0)
		for i := minLength; i <= n; i++ {
			start := i - minLength
			if start == 0 || (cut[start] && start < n) {
				running = (running + ways[start]) % mod
			}
			if cut[i] && i > 0 {
				next[i] = running
			}
		}
		ways = next
	}
	return ways[n]
}

var seed int64 = 2478

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strings := make([][]int64, 20)
	for t := range strings {
		d := []int64{2}
		for i := 0; i < 998; i++ {
			d = append(d, 1+nextRandom()%9)
		}
		strings[t] = append(d, 1)
	}
	check := int64(0)
	for p := int64(0); p < 90; p++ {
		for _, s := range strings {
			k := 1 + check%100
			m := 1 + check%5
			check = (check*31 + beautifulPartitions(s, k, m) + p) % mod
		}
	}
	fmt.Printf("90 passes over 20 strings of 1000: checksum %d\n", check)
}
