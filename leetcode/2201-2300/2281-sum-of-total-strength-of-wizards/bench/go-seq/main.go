// LeetCode #2281: Sum of Total Strength of Wizards -- the bench, the ★
// arm.
package main

import "fmt"

const mod = 1000000007

func totalStrength(strength []int64) int64 {
	n := int64(len(strength))
	left := make([]int64, n)
	right := make([]int64, n)
	stack := make([]int64, 0)
	for i := int64(0); i < n; i++ {
		for len(stack) > 0 && strength[stack[len(stack)-1]] >= strength[i] {
			stack = stack[:len(stack)-1]
		}
		left[i] = -1
		if len(stack) > 0 {
			left[i] = stack[len(stack)-1]
		}
		stack = append(stack, i)
	}
	stack = stack[:0]
	for i := n - 1; i >= 0; i-- {
		for len(stack) > 0 && strength[stack[len(stack)-1]] > strength[i] {
			stack = stack[:len(stack)-1]
		}
		right[i] = n
		if len(stack) > 0 {
			right[i] = stack[len(stack)-1]
		}
		stack = append(stack, i)
	}
	prefix := make([]int64, n+1)
	for i := int64(0); i < n; i++ {
		prefix[i+1] = (prefix[i] + strength[i]) % mod
	}
	twice := make([]int64, n+2)
	for i := int64(0); i < n+1; i++ {
		twice[i+1] = (twice[i] + prefix[i]) % mod
	}
	var total int64
	for i := int64(0); i < n; i++ {
		l, r := left[i], right[i]
		ends := (i - l) * ((twice[r+1] - twice[i+1] + mod) % mod) % mod
		starts := (r - i) * ((twice[i+1] - twice[l+1] + mod) % mod) % mod
		groups := (ends - starts + mod) % mod
		total = (total + strength[i]%mod*groups) % mod
	}
	return total
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2281

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 30; t++ {
		strength := make([]int64, 0)
		for i := 0; i < 100000; i++ {
			high := nextRandom()
			strength = append(strength, (high*32768+nextRandom())%1000000000+1)
		}
		check = (check*31 + totalStrength(strength)) % 1000000007
	}
	fmt.Printf("30 armies of 10^5: checksum %d\n", check)
}
