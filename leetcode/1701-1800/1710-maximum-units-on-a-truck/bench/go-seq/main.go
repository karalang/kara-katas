// LeetCode #1710: Maximum Units on a Truck -- the Go mirror of the bench
// (units.kara): the box types sorted by units, most first, and boxes
// taken from the front until the truck is full, on 1000 random problems
// of 1000 box types, each answered 10 times.
package main

import (
	"fmt"
	"sort"
)

func maximumUnits(boxTypes [][]int32, truckSize int32) int32 {
	order := make([][]int32, len(boxTypes))
	for i, t := range boxTypes {
		order[i] = append([]int32(nil), t...)
	}
	sort.SliceStable(order, func(a, b int) bool { return order[a][1] > order[b][1] })
	room := truckSize
	var total int32
	for _, t := range order {
		take := min(t[0], room)
		total += take * t[1]
		room -= take
		if room == 0 {
			break
		}
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 1000
	var rounds int64 = 10
	n := 1000
	var seed int64 = 1710
	problems := make([][][]int32, count)
	sizes := make([]int32, count)
	for p := 0; p < count; p++ {
		problems[p] = make([][]int32, n)
		for i := 0; i < n; i++ {
			b := nextRandom(&seed)%1000 + 1
			u := nextRandom(&seed)%1000 + 1
			problems[p][i] = []int32{int32(b), int32(u)}
		}
		a := nextRandom(&seed)
		sizes[p] = int32((a*32768+nextRandom(&seed))%1000000 + 1)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for p := 0; p < count; p++ {
			answer := int64(maximumUnits(problems[p], sizes[p]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d box types, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
