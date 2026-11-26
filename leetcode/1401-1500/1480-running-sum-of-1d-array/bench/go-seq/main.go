// LeetCode #1480: Running Sum of 1d Array -- bench, Go mirror of
// running_sum.kara
package main

import "fmt"

func runningSum(nums []int32) []int32 {
	var sums []int32
	var sum int32
	for _, x := range nums {
		sum += x
		sums = append(sums, sum)
	}
	return sums
}

var seed int64 = 1480

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int32, 1000)
	for p := range arrays {
		arrays[p] = make([]int32, 1000)
		for i := range arrays[p] {
			hi := nextRandom()
			arrays[p][i] = int32((hi*32768+nextRandom())%2000001 - 1000000)
		}
	}
	var check int64
	for pass := int64(0); pass < 200; pass++ {
		for p := 0; p < 1000; p++ {
			arrays[p][check%1000] = int32((check/7)%2000001 - 1000000)
			sums := runningSum(arrays[p])
			var s int64
			for j, x := range sums {
				s += int64(x) * int64(j+1)
			}
			check = (check*31 + s%1000000007 + 1000000007 + pass) % 1000000007
		}
	}
	fmt.Printf("200 passes over 1000 arrays of 1000 values: checksum %d\n", check)
}
