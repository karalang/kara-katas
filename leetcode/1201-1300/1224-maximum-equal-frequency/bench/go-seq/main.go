// LeetCode #1224 bench, Go mirror of the Kāra ★ arm: each number's count
// and how many numbers have each count, over 10 random arrays of 10^5
// numbers drawn once, 5 passes; checksum of the answers.
package main

import "fmt"

var seed int64 = 1224

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maxEqualFreq(nums []int64) int64 {
	top := nums[0]
	for _, x := range nums {
		if x > top {
			top = x
		}
	}
	count := make([]int64, top+1)
	withCount := make([]int64, len(nums)+1)
	var most, best int64
	for k, x := range nums {
		withCount[count[x]]--
		count[x]++
		withCount[count[x]]++
		if count[x] > most {
			most = count[x]
		}
		length := int64(k) + 1
		if most == 1 || withCount[most]*most+1 == length || (withCount[most-1]+1)*(most-1)+1 == length {
			best = length
		}
	}
	return best
}

func main() {
	arrays := make([][]int64, 10)
	for a := 0; a < 10; a++ {
		values := int64(2) << a
		arrays[a] = make([]int64, 100000)
		for k := range arrays[a] {
			arrays[a][k] = nextRandom()%values + 1
		}
	}
	var total, check int64
	for pass := 0; pass < 5; pass++ {
		for _, nums := range arrays {
			answer := maxEqualFreq(nums)
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("10 arrays of 10^5 numbers, 5 passes: lengths total %d, checksum %d\n", total, check)
}
