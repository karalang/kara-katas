// LeetCode #2007: Find Original Array From Doubled Array -- the ★ arm's
// benchmark, a mirror of doubled.kara.
package main

import "fmt"

func findOriginalArray(changed []int64) []int64 {
	if len(changed)%2 == 1 {
		return nil
	}
	top := changed[0]
	for _, x := range changed {
		if x > top {
			top = x
		}
	}
	count := make([]int64, top+1)
	for _, x := range changed {
		count[x]++
	}
	if count[0]%2 == 1 {
		return nil
	}
	var original []int64
	for i := int64(0); i < count[0]/2; i++ {
		original = append(original, 0)
	}
	for v := int64(1); v <= top; v++ {
		c := count[v]
		if c == 0 {
			continue
		}
		if 2*v > top || count[2*v] < c {
			return nil
		}
		count[2*v] -= c
		for i := int64(0); i < c; i++ {
			original = append(original, v)
		}
	}
	return original
}

var seed int64 = 2007

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 2000)
	for a := 0; a < 2000; a++ {
		var changed []int64
		for i := 0; i < 500; i++ {
			x := nextRandom() % 5001
			changed = append(changed, x, 2*x)
		}
		for i := int64(len(changed) - 1); i >= 1; i-- {
			j := nextRandom() % (i + 1)
			changed[i], changed[j] = changed[j], changed[i]
		}
		if nextRandom()%3 == 0 {
			i := nextRandom() % int64(len(changed))
			changed[i]++
		}
		arrays = append(arrays, changed)
	}
	var calls, sum, check int64
	for r := 0; r < 25; r++ {
		for _, changed := range arrays {
			original := findOriginalArray(changed)
			total := int64(len(original))
			for _, v := range original {
				total += v
			}
			calls++
			sum += total
			check = (check*31 + total) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
