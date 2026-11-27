// LeetCode #1835: Find XOR Sum of All Pairs Bitwise AND -- the bench in Go: the ★ arm over
// 3000 calls on pairs of 20 lists of 10^5 numbers from 0 to 10^9, built
// once, each call's two lists drawn from the checksum so far. The arm
// borrows both lists, so no call copies one.
package main

import "fmt"

func getXorSum(arr1, arr2 []int64) int64 {
	var left int64
	for _, a := range arr1 {
		left ^= a
	}
	var right int64
	for _, b := range arr2 {
		right ^= b
	}
	return left & right
}

func main() {
	seed := int64(1835)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	lists := make([][]int64, 0, 20)
	for l := 0; l < 20; l++ {
		list := make([]int64, 0, 100000)
		for k := 0; k < 100000; k++ {
			hi := nextRandom()
			list = append(list, (hi*32768+nextRandom())%1000000001)
		}
		lists = append(lists, list)
	}
	var check int64
	for call := int64(0); call < 3000; call++ {
		i := (check + call) % 20
		j := (check/20 + call*7) % 20
		check = (check*31 + getXorSum(lists[i], lists[j])) % 1000000007
	}
	fmt.Printf("3000 calls: checksum %d\n", check)
}
