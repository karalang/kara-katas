// LeetCode #1346 bench in Go: the ★ arm (a map of the values seen so far,
// each new value checked for its double and, when even, its half) on the
// same 2000 arrays of 500 values and 100 passes.
package main

import "fmt"

func checkIfExist(arr []int32) bool {
	seen := make(map[int32]struct{})
	for _, x := range arr {
		if _, ok := seen[2*x]; ok {
			return true
		}
		if x%2 == 0 {
			if _, ok := seen[x/2]; ok {
				return true
			}
		}
		seen[x] = struct{}{}
	}
	return false
}

var seed int64 = 1346

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int32, 2000)
	for a := range arrays {
		arrays[a] = make([]int32, 500)
		for i := range arrays[a] {
			arrays[a][i] = int32(2*(nextRandom()%1000) - 999)
		}
	}
	var check int64
	for pass := int64(0); pass < 100; pass++ {
		for a := 0; a < 2000; a++ {
			arrays[a][check%500] = int32((check/7)%2001 - 1000)
			var answer int64 = 1
			if checkIfExist(arrays[a]) {
				answer = 2
			}
			check = (check*31 + answer + pass) % 1000000007
		}
	}
	fmt.Printf("100 passes over 2000 arrays of 500: checksum %d\n", check)
}
