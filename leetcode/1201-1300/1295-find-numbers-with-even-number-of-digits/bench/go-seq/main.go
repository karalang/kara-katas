// LeetCode #1295 bench: the ★ arm over 200 arrays of 500 numbers up to 10^5,
// built once; then 500 passes, each setting one number of every array from
// the checksum so far and answering it.
package main

import "fmt"

func findNumbers(nums []int64) int64 {
	var even int64
	for _, x := range nums {
		digits := 0
		for rest := x; rest > 0; rest /= 10 {
			digits++
		}
		if digits%2 == 0 {
			even++
		}
	}
	return even
}

func main() {
	seed := int64(1295)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	arrays := make([][]int64, 200)
	for a := range arrays {
		arrays[a] = make([]int64, 500)
		for i := range arrays[a] {
			digits := nextRandom()%6 + 1
			low := int64(1)
			for d := int64(1); d < digits; d++ {
				low *= 10
			}
			if digits == 6 {
				arrays[a][i] = 100000
			} else {
				r := nextRandom()
				arrays[a][i] = low + (r*32768+nextRandom())%(9*low)
			}
		}
	}
	var check int64
	for p := int64(0); p < 500; p++ {
		for a := range arrays {
			arrays[a][check%500] = 1 + check%100000
			check = (check*31 + findNumbers(arrays[a]) + p) % 1000000007
		}
	}
	fmt.Printf("500 passes over 200 arrays of 500: checksum %d\n", check)
}
