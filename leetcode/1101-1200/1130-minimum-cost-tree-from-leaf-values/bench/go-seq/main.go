// LeetCode #1130: Minimum Cost Tree From Leaf Values -- the bench in Go,
// the ★ arm over []int64 leaves with a slice stack, the same 4096 arrays
// and 400 rounds.
package main

import "fmt"

func mctFromLeafValues(arr []int64) int64 {
	var cost int64
	stack := []int64{}
	for _, a := range arr {
		for len(stack) > 0 && stack[len(stack)-1] <= a {
			mid := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			partner := a
			if len(stack) > 0 {
				partner = min(stack[len(stack)-1], a)
			}
			cost += mid * partner
		}
		stack = append(stack, a)
	}
	for len(stack) > 1 {
		top := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		cost += top * stack[len(stack)-1]
	}
	return cost
}

var seed int64 = 1130

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := [][]int64{}
	for j := 0; j < 4096; j++ {
		arr := make([]int64, 40)
		for i := range arr {
			arr[i] = nextRandom()%15 + 1
		}
		arrays = append(arrays, arr)
	}
	var total, check int64
	for round := int64(0); round < 400; round++ {
		for j := int64(0); j < 4096; j++ {
			at := (round*7919 + j*104729) % 40
			arrays[j][at] = arrays[j][at]%15 + 1
			c := mctFromLeafValues(arrays[j])
			total += c
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("400 rounds over 4096 arrays of 40 leaves: costs total %d, checksum %d\n", total, check)
}
