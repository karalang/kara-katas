// LeetCode #2154: Keep Multiplying Found Values by Two -- the benchmark's
// Go mirror of doubling.kara.
package main

import "fmt"

func findFinalValue(nums []int64, original int64) int64 {
	found := make(map[int64]struct{})
	for _, x := range nums {
		found[x] = struct{}{}
	}
	value := original
	for {
		if _, ok := found[value]; !ok {
			break
		}
		value *= 2
	}
	return value
}

var seed int64 = 2154

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	row := make([]int64, 0, 400000)
	for i := 0; i < 400000; i++ {
		row = append(row, nextRandom()%1000+1)
	}
	var check int64
	for r := 0; r < 20000; r++ {
		a := nextRandom()
		b := nextRandom()
		start := (a*32768 + b) % 399001
		original := nextRandom()%1000 + 1
		value := findFinalValue(row[start:start+1000], original)
		check = (check*31 + value) % 1000000007
	}
	fmt.Printf("20000 solves: checksum %d\n", check)
}
