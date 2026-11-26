// LeetCode #1414 bench, Go: the Fibonacci numbers up to k, and the largest
// that fits taken each time, workload and checksum as
// find_min_fibonacci_numbers.kara.
package main

import "fmt"

func findMinFibonacciNumbers(k int32) int32 {
	fib := []int32{1, 1}
	for fib[len(fib)-1] <= k-fib[len(fib)-2] {
		fib = append(fib, fib[len(fib)-1]+fib[len(fib)-2])
	}
	left := k
	var count int32
	for i := len(fib) - 1; i >= 0; i-- {
		if fib[i] <= left {
			left -= fib[i]
			count++
		}
	}
	return count
}

func main() {
	var seed int64 = 1414
	var check int64
	for r := 0; r < 3000000; r++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		k := 1 + seed%1000000000
		check = (check*131 + int64(findMinFibonacciNumbers(int32(k)))) % 1000000007
	}
	fmt.Printf("3 * 10^6 values of k: checksum %d\n", check)
}
