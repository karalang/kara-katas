// Benchmark for #413: mirror of arithmetic_slices.kara (slices ending
// here).
package main

import (
	"fmt"
	"os"
	"strconv"
)

func numberOfArithmeticSlices(nums []int64) int64 {
	var ending, total int64
	for i := 2; i < len(nums); i++ {
		if nums[i]-nums[i-1] == nums[i-1]-nums[i-2] {
			ending++
			total += ending
		} else {
			ending = 0
		}
	}
	return total
}

var seed int64 = 413

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var rounds int64 = 60000
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	var n int64 = 5000
	nums := []int64{0}
	for int64(len(nums)) < n {
		diff := step()%7 - 3
		run := 1 + step()%30
		for k := int64(0); k < run; k++ {
			if int64(len(nums)) < n {
				last := nums[len(nums)-1]
				if last+diff > 1000 || last+diff < -1000 {
					diff = -diff
				}
				nums = append(nums, last+diff)
			}
		}
	}
	var total, checksum int64
	for r := int64(0); r < rounds; r++ {
		nums[r*7919%n] += r%3 - 1
		answer := numberOfArithmeticSlices(nums)
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d rounds on %d numbers: total %d, checksum %d\n", rounds, n, total, checksum)
}
