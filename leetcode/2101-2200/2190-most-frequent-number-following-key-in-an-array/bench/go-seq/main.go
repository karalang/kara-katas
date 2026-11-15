// LeetCode #2190: Most Frequent Number Following Key In an Array -- the
// benchmark's Go mirror of follow.kara, over a slice of the row: counts
// in a list, the leader kept as met.
package main

import "fmt"

func mostFrequent(nums []int64, key int64) int64 {
	counts := make([]int64, 1001)
	var best int64
	var target int64 = -1
	for i := 1; i < len(nums); i++ {
		if nums[i-1] == key {
			x := nums[i]
			counts[x]++
			if counts[x] > best {
				best = counts[x]
				target = x
			}
		}
	}
	return target
}

var seed int64 = 2190

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	a := nextRandom()
	b := nextRandom()
	return a*32768 + b
}

func main() {
	row := make([]int64, 1000000)
	for i := range row {
		row[i] = nextRandom()%100 + 1
	}
	var check int64
	for r := 0; r < 200000; r++ {
		start := bigRandom() % 999001
		key := row[start]
		check = (check*31 + mostFrequent(row[start:start+1000], key)) % 1000000007
	}
	fmt.Printf("200000 solves: checksum %d\n", check)
}
