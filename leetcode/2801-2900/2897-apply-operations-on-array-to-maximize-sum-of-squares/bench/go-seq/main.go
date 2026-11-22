// LeetCode #2897: Apply Operations on Array to Maximize Sum of Squares --
// the bench's Go mirror (squares.kara).
package main

import "fmt"

var seed int64 = 2897

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func maxSum(nums []int64, k int64) int64 {
	const modulus = 1000000007
	var holders [31]int64
	for _, v := range nums {
		for b := 0; b < 31; b++ {
			if (v>>b)&1 == 1 {
				holders[b]++
			}
		}
	}
	var sum int64
	for t := int64(0); t < k; t++ {
		var value int64
		for b := 0; b < 31; b++ {
			if holders[b] > 0 {
				holders[b]--
				value |= 1 << b
			}
		}
		sum = (sum + value*value) % modulus
	}
	return sum
}

func main() {
	const count, rounds, n = 20, 20, 10000
	cases := make([][]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			if c%2 == 0 {
				nums = append(nums, wide()%1000000000+1)
			} else {
				a := nextRandom() % 30
				b := nextRandom() % 30
				nums = append(nums, (int64(1)<<a)|(int64(1)<<b))
			}
		}
		cases[c] = nums
		ks[c] = wide()%n + 1
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			s := maxSum(cases[c], ks[c])
			total += s
			check = (check*31 + s + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: sums total %d, checksum %d\n", count, n, rounds, total, check)
}
