// LeetCode #2289: Steps to Make Array Non-decreasing -- the bench, the ★
// arm in Go. A stack of the elements still standing to the left, each
// with the step at which it is removed.
package main

import "fmt"

type entry struct{ value, step int64 }

func totalSteps(nums []int64) int64 {
	stack := []entry{}
	var most int64
	for _, x := range nums {
		var step int64
		for len(stack) > 0 && stack[len(stack)-1].value <= x {
			if stack[len(stack)-1].step > step {
				step = stack[len(stack)-1].step
			}
			stack = stack[:len(stack)-1]
		}
		if len(stack) == 0 {
			step = 0
		} else {
			step++
		}
		if step > most {
			most = step
		}
		stack = append(stack, entry{x, step})
	}
	return most
}

var seed int64 = 2289

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 50)
	for a := range arrays {
		nums := make([]int64, 10000)
		for i := range nums {
			nums[i] = int64(i)*3 + nextRandom()%20000
		}
		arrays[a] = nums
	}
	var check int64
	for p := 0; p < 20; p++ {
		var total int64
		for _, nums := range arrays {
			total += totalSteps(nums)
		}
		check = (check*31 + total) % 1000000007
	}
	fmt.Printf("20 passes over 50 arrays of 10^4: checksum %d\n", check)
}
