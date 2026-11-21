// LeetCode #2454: Next Greater Element IV -- bench, Go mirror of
// second.kara: two monotonic stacks, the first waiting for one greater
// value and the second for another.
package main

import "fmt"

func secondGreaterElement(nums []int64) []int64 {
	n := len(nums)
	answer := make([]int64, n)
	for j := range answer {
		answer[j] = -1
	}
	first := []int{}
	second := []int{}
	for j := 0; j < n; j++ {
		for len(second) > 0 && nums[second[len(second)-1]] < nums[j] {
			answer[second[len(second)-1]] = nums[j]
			second = second[:len(second)-1]
		}
		cut := len(first)
		for cut > 0 && nums[first[cut-1]] < nums[j] {
			cut--
		}
		second = append(second, first[cut:]...)
		first = append(first[:cut], j)
	}
	return answer
}

var seed int64 = 2454

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n int64 = 100000
	arrays := make([][]int64, 10)
	for a := range arrays {
		nums := make([]int64, n)
		for i := range nums {
			hi := nextRandom()
			nums[i] = (hi*32768 + nextRandom()) % 1000000001
		}
		arrays[a] = nums
	}
	var check int64
	for p := int64(0); p < 20; p++ {
		for a := int64(0); a < 10; a++ {
			arrays[a][(p*7919+a)%n] = check % 1000000001
			for _, v := range secondGreaterElement(arrays[a]) {
				check = (check*31 + v + 1) % 1000000007
			}
			check = (check + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
