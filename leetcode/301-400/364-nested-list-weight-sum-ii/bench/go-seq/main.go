// Benchmark for #364 -- mirror of weight_sum.kara.
package main

import "fmt"

type Nested struct {
	isInt bool
	v     int64
	list  []Nested
}

func maxDepth(list []Nested, depth int64) int64 {
	var deepest int64
	for i := range list {
		if list[i].isInt {
			deepest = max(deepest, depth)
		} else {
			deepest = max(deepest, maxDepth(list[i].list, depth+1))
		}
	}
	return deepest
}

func weighted(list []Nested, depth, top int64) int64 {
	var total int64
	for i := range list {
		if list[i].isInt {
			total += list[i].v * (top - depth + 1)
		} else {
			total += weighted(list[i].list, depth+1, top)
		}
	}
	return total
}

func depthSumInverse(list []Nested) int64 {
	return weighted(list, 1, maxDepth(list, 1))
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func build(seed *int64, depth int64) []Nested {
	n := next(seed) % 13
	var out []Nested
	for i := int64(0); i < n; i++ {
		if depth < 14 && next(seed)%3 == 0 {
			out = append(out, Nested{list: build(seed, depth+1)})
		} else {
			out = append(out, Nested{isInt: true, v: next(seed)%201 - 100})
		}
	}
	return out
}

func main() {
	var seed int64 = 364
	var checksum int64
	for t := 0; t < 10; t++ {
		list := build(&seed, 1)
		for r := 0; r < 20; r++ {
			checksum = (checksum*31 + depthSumInverse(list) + 1000000000000000) % 1000000007
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
