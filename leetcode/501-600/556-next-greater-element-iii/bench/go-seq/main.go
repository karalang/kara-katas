// Benchmark for #556: Go mirror of the ★ arm (the next permutation of the
// digits); see ../next_greater_element_iii.kara.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func nextGreaterElement(n int64) int64 {
	d := []int64{}
	for x := n; x > 0; x /= 10 {
		d = append(d, x%10)
	}
	for a, b := 0, len(d)-1; a < b; a, b = a+1, b-1 {
		d[a], d[b] = d[b], d[a]
	}
	i := len(d) - 2
	for i >= 0 && d[i] >= d[i+1] {
		i--
	}
	if i < 0 {
		return -1
	}
	j := len(d) - 1
	for d[j] <= d[i] {
		j--
	}
	d[i], d[j] = d[j], d[i]
	for a, b := i+1, len(d)-1; a < b; a, b = a+1, b-1 {
		d[a], d[b] = d[b], d[a]
	}
	var out int64
	for _, v := range d {
		out = out*10 + v
	}
	if out > 2147483647 {
		return -1
	}
	return out
}

func main() {
	count := 500000
	seed := int64(556)
	numbers := make([]int64, 0, count)
	for t := 0; t < count; t++ {
		var top int64 = 2147483647
		if t%3 == 0 {
			top = 1000
		} else if t%3 == 1 {
			top = 10000000
		}
		a := nextRandom(&seed)
		b := nextRandom(&seed)
		numbers = append(numbers, 1+(a*65536+b)%top)
	}
	found := 0
	var checksum int64
	for round := 0; round < 20; round++ {
		for g := 0; g < count; g++ {
			got := nextGreaterElement(numbers[(round*7+g)%count])
			if got > 0 {
				found++
			}
			checksum = (checksum*31 + got + 1) % 1000000007
		}
	}
	fmt.Printf("%d numbers, 20 rounds each: %d have a next, checksum %d\n", count, found, checksum)
}
