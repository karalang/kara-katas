// benchmark's Go mirror of replace.kara (LeetCode #2197, the ★ arm): a
// stack merged at its top.
package main

import "fmt"

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func replaceNonCoprimes(nums []int64) []int64 {
	stack := []int64{}
	for _, x := range nums {
		cur := x
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			g := gcd(top, cur)
			if g == 1 {
				break
			}
			cur = top / g * cur
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, cur)
	}
	return stack
}

var seed int64 = 2197

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func divisors(m int64) []int64 {
	out := []int64{}
	for d := int64(1); d <= 100000; d++ {
		if m%d == 0 {
			out = append(out, d)
		}
	}
	return out
}

func main() {
	pools := [][]int64{divisors(10810800), divisors(1674432), {1, 99991, 99989, 99971, 99961, 99929, 99923}}
	arrays := [][]int64{}
	for a := 0; a < 12; a++ {
		pool := pools[a%3]
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = pool[wideRandom()%int64(len(pool))]
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for pass := 0; pass < 100; pass++ {
		for _, nums := range arrays {
			out := replaceNonCoprimes(nums)
			check = (check*31 + int64(len(out))) % 1000000007
			check = (check*31 + out[len(out)/2]) % 1000000007
		}
	}
	fmt.Printf("100 passes over 12 arrays: checksum %d\n", check)
}
