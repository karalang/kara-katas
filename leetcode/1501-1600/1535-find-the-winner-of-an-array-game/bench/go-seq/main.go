// LeetCode #1535: Find the Winner of an Array Game -- bench: the ★ arm
// over 100 random arrays of 100000 distinct values, each with its own k
// from 1 to 200000, built once and answered 20 times. Go mirror of
// winner.kara.
package main

import "fmt"

func getWinner(arr []int64, k int64) int64 {
	front, streak := arr[0], int64(0)
	for i := 1; i < len(arr); i++ {
		if arr[i] > front {
			front = arr[i]
			streak = 1
		} else {
			streak++
		}
		if streak == k {
			return front
		}
	}
	return front
}

var seed int64 = 1535

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func draw(below int64) int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % below
}

func main() {
	const n = 100000
	arrs := make([][]int64, 100)
	ks := make([]int64, 100)
	for p := 0; p < 100; p++ {
		arr := make([]int64, n)
		for v := int64(1); v <= n; v++ {
			arr[v-1] = v * 3
		}
		for i := int64(n - 1); i >= 1; i-- {
			j := draw(i + 1)
			arr[i], arr[j] = arr[j], arr[i]
		}
		arrs[p] = arr
		ks[p] = draw(200000) + 1
	}
	var check int64
	for pass := 0; pass < 20; pass++ {
		for p := 0; p < 100; p++ {
			check = mix(check, getWinner(arrs[p], ks[p]))
		}
	}
	fmt.Printf("20 passes over 100 arrays of 100000 values: checksum %d\n", check)
}
