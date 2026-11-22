// LeetCode #2731: Movement of Robots -- the bench (robots.kara in Go): the
// places after d seconds, robots passing through each other in effect,
// sorted, each adding its distance to all those before it.
package main

import (
	"fmt"
	"slices"
)

const mod = 1000000007

func sumDistance(nums []int64, s string, d int64) int64 {
	places := make([]int64, 0, len(nums))
	for i := range nums {
		if s[i] == 'L' {
			places = append(places, nums[i]-d)
		} else {
			places = append(places, nums[i]+d)
		}
	}
	slices.Sort(places)
	var total, before int64
	for k := range places {
		total = (total + int64(k)*places[k] - before) % mod
		before += places[k]
	}
	return total
}

var seed int64 = 2731

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	nums []int64
	s    string
	d    int64
}

func main() {
	const cases, n, rounds = 10, 100000, 10
	problems := []problem{}
	for c := 0; c < cases; c++ {
		nums := make([]int64, n)
		at := int64(-2000000000)
		for i := 0; i < n; i++ {
			nums[i] = at
			at += (nextRandom()*32768+nextRandom())%40000 + 1
		}
		for i := int64(n - 1); i >= 1; i-- {
			j := nextRandom() % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		b := make([]byte, n)
		for i := range b {
			if nextRandom()%2 == 0 {
				b[i] = 'L'
			} else {
				b[i] = 'R'
			}
		}
		hi := nextRandom()
		d := (hi*32768 + nextRandom()) % 1000000001
		problems = append(problems, problem{nums, string(b), d})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range problems {
			total := sumDistance(p.nums, p.s, p.d)
			sum += total
			check = (check*31 + total + r) % 1000000007
		}
	}
	fmt.Printf("%d cases of %d robots, %d rounds: sums mod p sum to %d, checksum %d\n", cases, n, rounds, sum, check)
}
