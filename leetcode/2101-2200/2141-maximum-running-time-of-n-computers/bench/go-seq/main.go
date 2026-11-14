// LeetCode #2141: Maximum Running Time of N Computers -- the benchmark, the
// same algorithm as running.kara.
package main

import "fmt"

func maxRunTime(n int64, batteries []int64) int64 {
	total := int64(0)
	for _, b := range batteries {
		total += b
	}
	low, high := int64(0), total/n
	for low < high {
		mid := (low + high + 1) / 2
		usable := int64(0)
		for _, b := range batteries {
			if b < mid {
				usable += b
			} else {
				usable += mid
			}
		}
		if usable >= n*mid {
			low = mid
		} else {
			high = mid - 1
		}
	}
	return low
}

var seed int64 = 2141

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	fleets := make([][]int64, 10)
	for f := range fleets {
		fleets[f] = make([]int64, 100000)
		for i := range fleets[f] {
			hi := nextRandom()
			fleets[f][i] = (hi*32768+nextRandom())%1000000000 + 1
		}
	}
	total, check := int64(0), int64(0)
	for round := int64(0); round < 20; round++ {
		for f := 0; f < 10; f++ {
			hi := nextRandom()
			at := (hi*32768 + nextRandom()) % 100000
			hi = nextRandom()
			fleets[f][at] = (hi*32768+nextRandom())%1000000000 + 1
			minutes := maxRunTime(10000*int64(f+1), fleets[f])
			total += minutes
			check = (check*31 + minutes%1000000007 + round) % 1000000007
		}
	}
	fmt.Printf("200 solves: %d minutes in all, checksum %d\n", total, check)
}
