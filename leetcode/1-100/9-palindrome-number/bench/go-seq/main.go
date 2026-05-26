// LeetCode 9 — half-reverse Palindrome Number, Go seq mirror.
package main

import "fmt"

func isPalindrome(x int32) bool {
	if x < 0 || (x%10 == 0 && x != 0) {
		return false
	}
	var reversed int32
	for x > reversed {
		reversed = reversed*10 + x%10
		x /= 10
	}
	return x == reversed || x == reversed/10
}

func manufacturePalindrome(v32 int32) int32 {
	lo := v32
	if lo < 0 {
		lo = -lo
	}
	fourRaw := lo % 10000
	four := fourRaw
	if four < 1000 {
		four += 1000
	}
	d0 := four % 10
	d1 := (four / 10) % 10
	d2 := (four / 100) % 10
	d3 := (four / 1000) % 10
	rev := d0*1000 + d1*100 + d2*10 + d3
	return four*10000 + rev
}

func main() {
	const n int64 = 1024
	const kIters int64 = 50_000_000

	inputs := make([]int32, n)
	for i := int64(0); i < n; i++ {
		raw := i*2654435769 + 305419896
		v32 := int32(raw)
		if i%16 == 0 {
			inputs[i] = manufacturePalindrome(v32)
		} else {
			inputs[i] = v32
		}
	}

	var sum int64
	for k := int64(0); k < kIters; k++ {
		idx := k % n
		if isPalindrome(inputs[idx]) {
			sum++
		}
	}
	fmt.Println(sum)
}
