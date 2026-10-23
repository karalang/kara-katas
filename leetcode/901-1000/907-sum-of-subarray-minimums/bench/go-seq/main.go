// LeetCode #907: Sum of Subarray Minimums -- bench program, Go.
//
// How far each element reaches, over 1,000,000 numbers from 1 to 30000
// built once. Each round sums the subarray minimums, folds the sum into a
// checksum and changes one number.
package main

import "fmt"

func sumSubarrayMins(arr []int64) int64 {
	n := int64(len(arr))
	left := make([]int64, n)
	right := make([]int64, n)
	stack := make([]int64, 0)
	for i := int64(0); i < n; i++ {
		for len(stack) > 0 && arr[stack[len(stack)-1]] >= arr[i] {
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			left[i] = i - stack[len(stack)-1]
		} else {
			left[i] = i + 1
		}
		stack = append(stack, i)
	}
	stack = stack[:0]
	for k := int64(0); k < n; k++ {
		i := n - 1 - k
		for len(stack) > 0 && arr[stack[len(stack)-1]] > arr[i] {
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			right[i] = stack[len(stack)-1] - i
		} else {
			right[i] = n - i
		}
		stack = append(stack, i)
	}
	var total int64
	for i := int64(0); i < n; i++ {
		total = (total + arr[i]*left[i]%1000000007*right[i]) % 1000000007
	}
	return total
}

var seed int64 = 907

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 1000000
	var rounds int64 = 40
	arr := make([]int64, n)
	for i := int64(0); i < n; i++ {
		arr[i] = 1 + nextRandom()%30000
	}
	var check int64
	for round := int64(0); round < rounds; round++ {
		got := sumSubarrayMins(arr)
		check = (check*31 + got) % 1000000007
		arr[round*7919%n] = 1 + nextRandom()%30000
	}
	fmt.Printf("%d rounds over %d numbers: checksum %d\n", rounds, n, check)
}
