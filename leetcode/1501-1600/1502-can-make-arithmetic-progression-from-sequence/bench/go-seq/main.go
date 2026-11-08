// LeetCode #1502: Can Make Arithmetic Progression From Sequence -- the
// benchmark, the same algorithm as progression.kara: a copy sorted, every
// gap equal to the first.
package main

import (
	"fmt"
	"slices"
)

func canMake(arr []int64) bool {
	a := make([]int64, len(arr))
	copy(a, arr)
	slices.Sort(a)
	d := a[1] - a[0]
	for i := 1; i < len(a)-1; i++ {
		if a[i+1]-a[i] != d {
			return false
		}
	}
	return true
}

var seed int64 = 1502

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func randomArray(most int64) []int64 {
	n := nextRandom()%(most-1) + 2
	kind := nextRandom() % 3
	arr := make([]int64, 0, n)
	if kind == 2 {
		spread := nextRandom()%50 + 1
		for i := int64(0); i < n; i++ {
			arr = append(arr, nextRandom()%spread-spread/2)
		}
	} else {
		start := nextRandom()%2001 - 1000
		d := nextRandom()%21 - 10
		for i := int64(0); i < n; i++ {
			arr = append(arr, start+i*d)
		}
		if kind == 1 {
			at := nextRandom() % n
			if nextRandom()%2 == 0 {
				arr[at]++
			} else {
				arr[at]--
			}
		}
	}
	for i := n - 1; i >= 1; i-- {
		j := nextRandom() % (i + 1)
		arr[i], arr[j] = arr[j], arr[i]
	}
	return arr
}

func main() {
	arrays := make([][]int64, 3000)
	for i := range arrays {
		arrays[i] = randomArray(1000)
	}
	var can, check int64
	for r := 0; r < 10; r++ {
		for _, arr := range arrays {
			var answer int64
			if canMake(arr) {
				answer = 1
			}
			can += answer
			check = mix(check, answer)
		}
	}
	fmt.Printf("30000 answers over 3000 arrays of 2 to 1000 numbers: %d can, checksum %d\n", can, check)
}
