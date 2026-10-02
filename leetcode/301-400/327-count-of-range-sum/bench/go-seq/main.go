// Benchmark workload for LeetCode #327 — Go mirror of count_range_sum.kara.
package main

import "fmt"

const (
	LEN     = 100000
	PUNCHES = 20
	MODULUS = 1073741789
)

func countAndSort(p, tmp []int64, lo, hi int, lower, upper int64) int64 {
	if hi-lo <= 1 {
		return 0
	}
	mid := lo + (hi-lo)/2
	count := countAndSort(p, tmp, lo, mid, lower, upper) + countAndSort(p, tmp, mid, hi, lower, upper)

	start, end := mid, mid
	for a := lo; a < mid; a++ {
		for start < hi && p[start] < p[a]+lower {
			start++
		}
		for end < hi && p[end] <= p[a]+upper {
			end++
		}
		count += int64(end - start)
	}

	i, j, k := lo, mid, lo
	for i < mid && j < hi {
		if p[i] <= p[j] {
			tmp[k] = p[i]
			i++
		} else {
			tmp[k] = p[j]
			j++
		}
		k++
	}
	for i < mid {
		tmp[k] = p[i]
		i++
		k++
	}
	for j < hi {
		tmp[k] = p[j]
		j++
		k++
	}
	for t := lo; t < hi; t++ {
		p[t] = tmp[t]
	}
	return count
}

func countRangeSum(nums []int64, lower, upper int64) int64 {
	p := []int64{0}
	var s int64
	for _, x := range nums {
		s += x
		p = append(p, s)
	}
	tmp := []int64{}
	for range p {
		tmp = append(tmp, 0)
	}
	return countAndSort(p, tmp, 0, len(p), lower, upper)
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var seed int64 = 327
	a := []int64{}
	for i := 0; i < LEN; i++ {
		a = append(a, next(&seed)%2001-1000)
	}
	var sink int64
	for r := 0; r < PUNCHES; r++ {
		pos := (next(&seed)*32768 + next(&seed)) % LEN
		a[pos] = next(&seed)%2001 - 1000
		w := next(&seed) % 1000
		count := countRangeSum(a, -w, w)
		sink = (sink*31 + count%MODULUS) % MODULUS
	}
	fmt.Printf("sink %d\n", sink)
}
