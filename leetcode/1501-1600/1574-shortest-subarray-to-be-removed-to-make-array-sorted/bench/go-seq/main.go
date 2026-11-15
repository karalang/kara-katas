// LeetCode #1574: Shortest Subarray to be Removed to Make Array Sorted --
// bench: the ★ arm (a sorted prefix joined to a sorted suffix by two
// pointers) over 20 arrays of 500000 values, each a rising first half, a
// stretch of random values and a rising second half that starts low, built
// once; then 3 rounds answering all 20, 60 answers.
package main

import "fmt"

func shortest(arr []int64) int64 {
	n := len(arr)
	left := 0
	for left+1 < n && arr[left] <= arr[left+1] {
		left++
	}
	if left == n-1 {
		return 0
	}
	right := n - 1
	for right > 0 && arr[right-1] <= arr[right] {
		right--
	}
	best := min(n-left-1, right)
	j := right
	for i := 0; i < left+1; i++ {
		for j < n && arr[j] < arr[i] {
			j++
		}
		best = min(best, j-i-1)
	}
	return int64(best)
}

var seed int64 = 1574

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 500000
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		middle := nextRandom()%1000 + 1
		start := (n - middle) / 2
		arr := make([]int64, 0)
		var v int64
		for i := int64(0); i < n; i++ {
			if i == start+middle {
				v = nextRandom() % 1000
			}
			if i >= start && i < start+middle {
				arr = append(arr, nextRandom()%4000000)
			} else {
				v += nextRandom() % 8
				arr = append(arr, v)
			}
		}
		arrays = append(arrays, arr)
	}
	var check, total int64
	for r := 0; r < 3; r++ {
		for _, arr := range arrays {
			length := shortest(arr)
			total += length
			check = mix(check, length)
		}
	}
	fmt.Printf("60 answers over 20 arrays of %d values: lengths total %d, checksum %d\n", n, total, check)
}
