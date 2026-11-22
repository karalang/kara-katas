// LeetCode #2848: Points That Intersect With Cars -- the bench,
// mirrored from points.kara: each car marks its points on a road of
// 100, and the marked ones are counted.
package main

import "fmt"

func numberOfPoints(nums [][2]int64) int64 {
	var covered [101]bool
	for _, car := range nums {
		for x := car[0]; x <= car[1]; x++ {
			covered[x] = true
		}
	}
	var count int64
	for _, c := range covered {
		if c {
			count++
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 10000, 50
	seed := int64(2848)
	parkings := make([][][2]int64, 0, count)
	for c := 0; c < count; c++ {
		cars := nextRandom(&seed)%100 + 1
		nums := make([][2]int64, 0, cars)
		for i := int64(0); i < cars; i++ {
			start := nextRandom(&seed)%100 + 1
			a := nextRandom(&seed)
			length := a % (nextRandom(&seed)%100 + 1)
			nums = append(nums, [2]int64{start, min(start+length, 100)})
		}
		parkings = append(parkings, nums)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range parkings {
			points := numberOfPoints(nums)
			total += points
			check = (check*31 + points + r) % 1000000007
		}
	}
	fmt.Printf("%d parkings, %d rounds: %d points, checksum %d\n", count, rounds, total, check)
}
