// Benchmark: LeetCode #1088 Confusing Number II -- mirrors
// confusing_number_ii.kara: a depth-first walk over the numbers made of the
// digits that rotate, each carrying its rotation, for 400 random n up to
// 10^9 drawn once.
package main

import "fmt"

func rotated(d int64) int64 {
	switch d {
	case 0:
		return 0
	case 1:
		return 1
	case 6:
		return 9
	case 8:
		return 8
	case 9:
		return 6
	}
	return -1
}

func countFrom(num, rot, unit, n int64) int64 {
	var total int64
	for _, d := range [5]int64{0, 1, 6, 8, 9} {
		next := num*10 + d
		if next > n {
			break
		}
		if next == 0 {
			continue
		}
		r := rotated(d)*unit + rot
		if next != r {
			total++
		}
		total += countFrom(next, r, unit*10, n)
	}
	return total
}

func confusingNumberII(n int64) int64 { return countFrom(0, 0, 1, n) }

var seed int64 = 1088

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	ns := make([]int64, 0, 400)
	for i := 0; i < 400; i++ {
		a := nextRandom()
		hi := a*32768 + nextRandom()
		ns = append(ns, hi%1000000000+1)
	}
	var total, check int64
	for _, n := range ns {
		a := confusingNumberII(n)
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("400 n up to 10^9: %d confusing numbers, checksum %d\n", total, check)
}
