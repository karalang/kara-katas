// Benchmark workload for LeetCode #254 — Factor Combinations (Go mirror).
// Mirrors factor_combinations.kara algorithm-for-algorithm.
package main

import "fmt"

var digest, total int64
var path []int64

func helper(remaining, start int64) {
	i := start
	for i*i <= remaining {
		if remaining%i == 0 {
			combo := make([]int64, len(path), len(path)+2)
			copy(combo, path)
			combo = append(combo, i, remaining/i)

			var h int64 = 1
			for _, x := range combo {
				h = (h*1000003 + x) % 1000000007
			}
			digest = (digest + h) % 1000000007
			total++

			path = append(path, i)
			helper(remaining/i, i)
			path = path[:len(path)-1]
		}
		i++
	}
}

func main() {
	var hi int64 = 150000
	for n := int64(2); n <= hi; n++ {
		path = path[:0]
		if n >= 4 {
			helper(n, 2)
		}
	}
	fmt.Println(total, digest)
}
