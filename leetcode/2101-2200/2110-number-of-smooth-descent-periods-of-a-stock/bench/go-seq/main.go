// LeetCode #2110: Number of Smooth Descent Periods of a Stock -- the
// benchmark, the same algorithm as descent.kara: the descent run's length
// up to each day, summed.
package main

import "fmt"

func getDescentPeriods(prices []int64) int64 {
	var run, total int64 = 1, 1
	for i := 1; i < len(prices); i++ {
		if prices[i-1]-prices[i] == 1 {
			run++
		} else {
			run = 1
		}
		total += run
	}
	return total
}

var seed int64 = 2110

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		var p int64 = 5000000
		prices := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			prices = append(prices, p)
			if nextRandom()%4 != 0 {
				p = p - 1
			} else {
				p = p + nextRandom()%20
			}
		}
		arrays = append(arrays, prices)
	}
	var total, check int64
	for round := 0; round < 10; round++ {
		for a := 0; a < 20; a++ {
			arrays[a][round*9973] += 1
			got := getDescentPeriods(arrays[a])
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("200 counts: %d periods, checksum %d\n", total, check)
}
