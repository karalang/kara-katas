// LeetCode #1310 bench, Go: the ★ arm (a prefix XOR, each answer the XOR of
// the prefixes at the range's two ends) on the same 10 arrays and 100
// passes.
package main

import "fmt"

func xorQueries(arr []int64, queries [][]int64) []int64 {
	prefix := make([]int64, len(arr)+1)
	for i := range arr {
		prefix[i+1] = prefix[i] ^ arr[i]
	}
	out := make([]int64, len(queries))
	for k, q := range queries {
		out[k] = prefix[q[1]+1] ^ prefix[q[0]]
	}
	return out
}

var seed int64 = 1310

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n, m int64 = 30000, 30000
	arrays := make([][]int64, 10)
	ranges := make([][][]int64, 10)
	for a := 0; a < 10; a++ {
		arr := make([]int64, n)
		for k := range arr {
			hi := nextRandom()
			lo := nextRandom()
			arr[k] = 1 + (hi*65536+lo)%1000000000
		}
		arrays[a] = arr
		queries := make([][]int64, m)
		for k := range queries {
			x := nextRandom() % n
			y := nextRandom() % n
			if x <= y {
				queries[k] = []int64{x, y}
			} else {
				queries[k] = []int64{y, x}
			}
		}
		ranges[a] = queries
	}
	var check int64
	for pass := int64(0); pass < 100; pass++ {
		for a := 0; a < 10; a++ {
			arrays[a][check%n] = 1 + (check/7)%1000000000
			x := (check / 11) % n
			y := (check / 13) % n
			if x <= y {
				ranges[a][check%m] = []int64{x, y}
			} else {
				ranges[a][check%m] = []int64{y, x}
			}
			got := xorQueries(arrays[a], ranges[a])
			check = (check*31 + got[(check/3)%m]) % 1000000007
			check = (check*31 + got[(check/17)%m] + pass) % 1000000007
		}
	}
	fmt.Printf("100 passes over 10 arrays of 3 * 10^4: checksum %d\n", check)
}
