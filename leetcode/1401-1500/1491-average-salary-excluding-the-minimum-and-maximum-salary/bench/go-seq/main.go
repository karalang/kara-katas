// LeetCode #1491: Average Salary Excluding the Minimum and Maximum Salary --
// the bench in Go, mirroring average.kara: one pass keeping the sum, the
// least and the most.
package main

import (
	"fmt"
	"math"
)

func average(salary []int32) float64 {
	least, most := salary[0], salary[0]
	var sum int64
	for _, s := range salary {
		if s < least {
			least = s
		}
		if s > most {
			most = s
		}
		sum += int64(s)
	}
	return float64(sum-int64(least)-int64(most)) / float64(len(salary)-2)
}

func main() {
	salary := make([]int32, 100)
	for k := int64(0); k < 100; k++ {
		salary[k] = int32(1000 + 9000*k)
	}
	var check int64
	for pass := int64(0); pass < 2000000; pass++ {
		k := pass % 100
		salary[k] = int32(1000 + 9000*k + (check+pass)%9000)
		cents := int64(math.Round(average(salary) * 100.0))
		check = (check*31 + cents) % 1000000007
	}
	fmt.Printf("2000000 calls: checksum %d\n", check)
}
