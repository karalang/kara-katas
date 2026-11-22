// LeetCode #2780: Minimum Index of a Valid Split -- the bench in Go: the
// ★ arm over 20 arrays of 10^5 numbers up to 10^9, each with a dominant
// number, all drawn first, then each answered 100 times.
package main

import "fmt"

func minimumIndex(nums []int64) int64 {
	n := int64(len(nums))
	var x, votes int64
	for _, v := range nums {
		if votes == 0 {
			x = v
		}
		if v == x {
			votes++
		} else {
			votes--
		}
	}
	var total int64
	for _, v := range nums {
		if v == x {
			total++
		}
	}
	var left int64
	for i := int64(0); i < n-1; i++ {
		if nums[i] == x {
			left++
		}
		if 2*left > i+1 && 2*(total-left) > n-i-1 {
			return i
		}
	}
	return -1
}

var seed int64 = 2780

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func dominated(n, others, top int64) []int64 {
	x := wide()%top + 1
	many := n/2 + 1 + wide()%(n-n/2)
	nums := make([]int64, 0, n)
	for int64(len(nums)) < many {
		nums = append(nums, x)
	}
	for int64(len(nums)) < n {
		v := wide()%others + 1
		if v != x {
			nums = append(nums, v)
		}
	}
	for i := n - 1; i > 0; i-- {
		j := wide() % (i + 1)
		nums[i], nums[j] = nums[j], nums[i]
	}
	return nums
}

func main() {
	count := 20
	rounds := 100
	cases := make([][]int64, count)
	for c := range cases {
		cases[c] = dominated(100000, 1000000000, 1000000000)
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, nums := range cases {
			a := minimumIndex(nums)
			total += a
			check = (check*31 + a + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 10^5, %d rounds: indices sum to %d, checksum %d\n", count, rounds, total, check)
}
