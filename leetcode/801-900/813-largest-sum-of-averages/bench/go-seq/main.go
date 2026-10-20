// LeetCode 813 -- Largest Sum of Averages: the bench, with the ★ arm's one
// row of prefix-sum DP.
package main

import "fmt"

var seed int64 = 813

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func largestSumOfAverages(nums []int64, k int64) float64 {
	n := len(nums)
	prefix := make([]int64, n+1)
	for i := 0; i < n; i++ {
		prefix[i+1] = prefix[i] + nums[i]
	}
	best := make([]float64, n+1)
	for i := 1; i <= n; i++ {
		best[i] = float64(prefix[i]) / float64(i)
	}
	for g := int64(1); g < k; g++ {
		for i := n; i >= 1; i-- {
			for p := 1; p < i; p++ {
				candidate := best[p] + float64(prefix[i]-prefix[p])/float64(i-p)
				if candidate > best[i] {
					best[i] = candidate
				}
			}
		}
	}
	return best[n]
}

// 64 arrays of 100 numbers from 1 to 10000 are made once. Each round writes
// a new number into one place of the next array and finds its largest sum
// of averages in at most k groups, k going round 1 to 100.
func main() {
	arrays := make([][]int64, 64)
	for a := range arrays {
		for i := 0; i < 100; i++ {
			arrays[a] = append(arrays[a], 1+nextRandom()%10000)
		}
	}
	var rounds int64 = 6000
	total := 0.0
	var check int64
	for r := int64(0); r < rounds; r++ {
		a := r % 64
		arrays[a][r/64%100] = 1 + nextRandom()%10000
		answer := largestSumOfAverages(arrays[a], 1+r%100)
		total += answer
		check = (check*131 + int64(answer*1000.0)) % 1000000007
	}
	fmt.Printf("%d rounds of 100 numbers: total %.5f, checksum %d\n", rounds, total, check)
}
