// Benchmark for #670: the last place of each digit, as the Kara ★ arm.
package main

import "fmt"

func digitsOf(num int64) []int64 {
	d := []int64{}
	for x := num; x > 0; x /= 10 {
		d = append(d, x%10)
	}
	if len(d) == 0 {
		d = append(d, 0)
	}
	for i, j := 0, len(d)-1; i < j; i, j = i+1, j-1 {
		d[i], d[j] = d[j], d[i]
	}
	return d
}

func numberOf(d []int64) int64 {
	x := int64(0)
	for _, v := range d {
		x = x*10 + v
	}
	return x
}

func maximumSwap(num int64) int64 {
	d := digitsOf(num)
	last := make([]int64, 10)
	for v := range last {
		last[v] = -1
	}
	for i, v := range d {
		last[v] = int64(i)
	}
	for i := range d {
		for v := int64(9); v > d[i]; v-- {
			if last[v] > int64(i) {
				j := last[v]
				d[j] = d[i]
				d[i] = v
				return numberOf(d)
			}
		}
	}
	return num
}

func main() {
	count := int64(3000000)
	sum := int64(0)
	for i := int64(0); i < count; i++ {
		sum = (sum*31 + maximumSwap(i*33+i%7)) % 1000000007
	}
	fmt.Printf("%d numbers: checksum %d\n", count, sum)
}
