// Benchmark harness for LeetCode #137 — Single Number II.
// Mirrors single_number.kara algorithm-for-algorithm.

package main

import "fmt"

func mask32() int64 {
	return 4294967295
}

func signExtend32(v int64) int64 {
	if v >= 2147483648 {
		return v - 4294967296
	}
	return v
}

func singleOnesTwos(nums []int64) int64 {
	mask := mask32()
	var ones int64 = 0
	var twos int64 = 0
	for i := 0; i < len(nums); i++ {
		x := nums[i] & mask
		ones = (ones ^ x) &^ twos & mask
		twos = (twos ^ x) &^ ones & mask
	}
	return signExtend32(ones)
}

func singleBitcount(nums []int64) int64 {
	var res int64 = 0
	for b := uint(0); b < 32; b++ {
		var cnt int64 = 0
		for i := 0; i < len(nums); i++ {
			if (nums[i]>>b)&1 == 1 {
				cnt++
			}
		}
		if cnt%3 != 0 {
			res |= int64(1) << b
		}
	}
	return signExtend32(res)
}

func main() {
	const np int64 = 4
	const k int64 = 30000
	const iters int64 = 40

	arrays := make([][]int64, 0, np)
	for j := int64(0); j < np; j++ {
		vals := make([]int64, 0, k)
		x := j + 1
		for t := int64(0); t < k; t++ {
			x = (x*1103515245 + 12345) % 2147483648
			hi := x / 65536
			x = (x*1103515245 + 12345) % 2147483648
			vals = append(vals, (hi*32768+x/65536)%100000)
		}
		arr := make([]int64, 0, 3*k+1)
		for pass := 0; pass < 3; pass++ {
			for q := int64(0); q < k; q++ {
				arr = append(arr, vals[q])
			}
		}
		arr = append(arr, 999983+j)
		arrays = append(arrays, arr)
	}

	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		idx := (it * 3) % np
		a := singleOnesTwos(arrays[idx])
		b := singleBitcount(arrays[idx])
		if a != b {
			sink += 1000000000
		}
		sink = (sink + a + b) % 1000000007
	}
	fmt.Println(sink)
}
