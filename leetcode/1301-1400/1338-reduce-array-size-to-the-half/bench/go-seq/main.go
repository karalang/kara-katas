// LeetCode #1338 bench, Go mirror of the Kāra bench: the ★ arm on 20
// arrays of 10^5 values built once, then 30 passes, each setting one value
// of every array from the checksum so far, answering every array.
package main

import (
	"fmt"
	"slices"
)

func minSetSize(arr []int32) int {
	counts := map[int32]int{}
	for _, x := range arr {
		counts[x]++
	}
	sizes := make([]int, 0, len(counts))
	for _, c := range counts {
		sizes = append(sizes, c)
	}
	slices.Sort(sizes)
	slices.Reverse(sizes)
	removed := 0
	chosen := 0
	for _, s := range sizes {
		if 2*removed >= len(arr) {
			break
		}
		removed += s
		chosen++
	}
	return chosen
}

var seed int64 = 1338

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	arrays := make([][]int32, 20)
	for t := range arrays {
		top := int64(100000)
		if t%2 == 1 {
			top = 1000
		}
		arr := make([]int32, n)
		for i := range arr {
			a := nextRandom()
			arr[i] = int32(1 + (a*32768+nextRandom())%top)
		}
		arrays[t] = arr
	}
	var check int64
	for pass := int64(0); pass < 30; pass++ {
		for t := 0; t < 20; t++ {
			at := check % n
			arrays[t][at] = int32(1 + check/3%1000)
			answer := minSetSize(arrays[t])
			check = (check*31 + int64(answer) + pass) % 1000000007
		}
	}
	fmt.Printf("30 passes over 20 arrays of 10^5: checksum %d\n", check)
}
