// LeetCode #2172: Maximum AND Sum of Array -- the benchmark's Go mirror of
// and_sum.kara.
package main

import "fmt"

func maximumAndSum(nums []int64, numSlots int64) int64 {
	powers := make([]int64, 0, numSlots)
	p := int64(1)
	for k := int64(0); k < numSlots; k++ {
		powers = append(powers, p)
		p *= 3
	}
	best := make([]int64, p)
	for i := range best {
		best[i] = -1
	}
	best[0] = 0
	var answer int64
	for fill := int64(0); fill < p; fill++ {
		if best[fill] < 0 {
			continue
		}
		var placed int64
		for rest := fill; rest > 0; rest /= 3 {
			placed += rest % 3
		}
		if placed == int64(len(nums)) {
			if best[fill] > answer {
				answer = best[fill]
			}
			continue
		}
		for slot := int64(0); slot < numSlots; slot++ {
			if fill/powers[slot]%3 < 2 {
				next := fill + powers[slot]
				sum := best[fill] + (nums[placed] & (slot + 1))
				if sum > best[next] {
					best[next] = sum
				}
			}
		}
	}
	return answer
}

var seed int64 = 2172

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	row := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		row = append(row, nextRandom()%15+1)
	}
	var check int64
	for r := 0; r < 200; r++ {
		start := nextRandom() % 99983
		best := maximumAndSum(row[start:start+18], 9)
		check = (check*31 + best) % 1000000007
	}
	fmt.Printf("200 solves: checksum %d\n", check)
}
