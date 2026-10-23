// LeetCode #873 bench: Go mirror of len_longest_fib_subseq.kara (the ★
// arm, a map from value to index) on the same 100 arrays.
package main

import (
	"fmt"
	"sort"
)

func lenLongestFibSubseq(arr []int64) int64 {
	n := len(arr)
	index := make(map[int64]int)
	for i, x := range arr {
		index[x] = i
	}
	longest := make([][]int64, n)
	for i := range longest {
		longest[i] = make([]int64, n)
		for j := range longest[i] {
			longest[i][j] = 2
		}
	}
	var best int64
	for k := 0; k < n; k++ {
		for j := 0; j < k; j++ {
			before := arr[k] - arr[j]
			if before < arr[j] {
				if i, ok := index[before]; ok {
					longest[j][k] = longest[i][j] + 1
					if longest[j][k] > best {
						best = longest[j][k]
					}
				}
			}
		}
	}
	return best
}

var seed int64 = 873

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func increasing(n int, gap int64) []int64 {
	arr := make([]int64, 0, n)
	var x int64
	for i := 0; i < n; i++ {
		x += 1 + nextRandom()%gap
		arr = append(arr, x)
	}
	return arr
}

func big() int64 {
	hi := nextRandom()
	return (hi*32768+nextRandom())%1000000000 + 1
}

func scattered(n, run int) []int64 {
	a := nextRandom()%1000 + 1
	b := a + nextRandom()%1000 + 1
	vals := []int64{a, b}
	for len(vals) < run && a+b <= 1000000000 {
		a, b = b, a+b
		vals = append(vals, b)
	}
	for len(vals) < n {
		vals = append(vals, big())
	}
	sort.Slice(vals, func(i, j int) bool { return vals[i] < vals[j] })
	arr := make([]int64, 0, len(vals))
	for _, x := range vals {
		if len(arr) == 0 || arr[len(arr)-1] != x {
			arr = append(arr, x)
		}
	}
	return arr
}

func main() {
	arrays := make([][]int64, 0, 100)
	for k := 0; k < 100; k++ {
		if k%2 == 0 {
			arrays = append(arrays, increasing(1000, int64(k%5+2)))
		} else {
			arrays = append(arrays, scattered(1000, 10+k%30))
		}
	}
	var total, check int64
	for _, arr := range arrays {
		answer := lenLongestFibSubseq(arr)
		total += answer
		check = (check*131 + answer) % 1000000007
	}
	fmt.Printf("100 arrays of 1000 values: lengths sum to %d, checksum %d\n", total, check)
}
