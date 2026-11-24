// LeetCode #2535 bench, Go mirror of difference.kara.
package main

import "fmt"

var seed int64 = 2535

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func differenceOfSum(nums []int64) int64 {
	var elementSum, digitSum int64
	for _, x := range nums {
		elementSum += x
		rest := x
		for rest > 0 {
			digitSum += rest % 10
			rest /= 10
		}
	}
	d := elementSum - digitSum
	if d < 0 {
		return -d
	}
	return d
}

func main() {
	const passes, n int64 = 1000, 2000
	lists := make([][]int64, 50)
	for q := range lists {
		lists[q] = make([]int64, n)
		for i := range lists[q] {
			lists[q][i] = nextRandom()%2000 + 1
		}
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for q := 0; q < 50; q++ {
			at := check % n
			lists[q][at] = (check+p)%2000 + 1
			check = (check*31 + differenceOfSum(lists[q]) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 50 lists of 2000: checksum %d\n", passes, check)
}
