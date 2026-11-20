// LeetCode #1213 bench, in Go: the ★ arm (three pointers, all three
// stepping on when the values agree and otherwise only those at the least
// value) on 1000 triples of arrays of 600 to 950 values drawn once, then
// 10 rounds over the triples, every answer's length and last value folded
// into a checksum.
package main

import "fmt"

var seed int64 = 1213

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomSorted(percent int64) []int64 {
	out := []int64{}
	for v := int64(1); v <= 2000; v++ {
		if nextRandom()%100 < percent {
			out = append(out, v)
		}
	}
	return out
}

func arraysIntersection(arr1, arr2, arr3 []int64) []int64 {
	out := []int64{}
	i, j, k := 0, 0, 0
	for i < len(arr1) && j < len(arr2) && k < len(arr3) {
		a, b, c := arr1[i], arr2[j], arr3[k]
		if a == b && b == c {
			out = append(out, a)
			i++
			j++
			k++
		} else {
			least := min(a, b, c)
			if a == least {
				i++
			}
			if b == least {
				j++
			}
			if c == least {
				k++
			}
		}
	}
	return out
}

func main() {
	triples := make([][3][]int64, 1000)
	for t := range triples {
		for s := 0; s < 3; s++ {
			triples[t][s] = randomSorted(33 + nextRandom()%12)
		}
	}
	var check int64
	for round := int64(0); round < 10; round++ {
		for _, t := range triples {
			answer := arraysIntersection(t[0], t[1], t[2])
			var last int64
			if len(answer) > 0 {
				last = answer[len(answer)-1]
			}
			check = (check*131 + int64(len(answer)) + last + round) % 1000000007
		}
	}
	fmt.Printf("10 rounds over 1000 triples of 600 to 950 values: checksum %d\n", check)
}
