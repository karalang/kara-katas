// LeetCode #2037: Minimum Number of Moves to Seat Everyone -- the ★ arm in
// Go, the same algorithm and workload as seats.kara: both lists copied and
// sorted (slices.Sort), the k-th seat paired with the k-th student, the
// distances summed.
package main

import (
	"fmt"
	"slices"
)

func minMovesToSeat(seats, students []int64) int64 {
	slices.Sort(seats)
	slices.Sort(students)
	var moves int64
	for k := range seats {
		d := seats[k] - students[k]
		if d < 0 {
			d = -d
		}
		moves += d
	}
	return moves
}

var seed int64 = 2037

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	seats := make([][]int64, 2000)
	students := make([][]int64, 2000)
	for r := 0; r < 2000; r++ {
		a := make([]int64, 100)
		for i := range a {
			a[i] = nextRandom()%100 + 1
		}
		b := make([]int64, 100)
		for i := range b {
			b[i] = nextRandom()%100 + 1
		}
		seats[r] = a
		students[r] = b
	}
	var calls, sum, check int64
	for round := int64(0); round < 25; round++ {
		for r := int64(0); r < 2000; r++ {
			at := (round*37 + r*11) % 100
			seats[r][at] = seats[r][at]%100 + 1
			answer := minMovesToSeat(slices.Clone(seats[r]), slices.Clone(students[r]))
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
