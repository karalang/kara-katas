// LeetCode #989: Add to Array-Form of Integer -- bench, the ★ arm
// (k carried in from the last digit), the same algorithm and workload
// as add_to_array_form.kara.
package main

import "fmt"

func addToArrayForm(num []int64, k int64) []int64 {
	var out []int64
	carry := k
	i := len(num) - 1
	for i >= 0 || carry > 0 {
		if i >= 0 {
			carry += num[i]
			i--
		}
		out = append(out, carry%10)
		carry /= 10
	}
	for a, b := 0, len(out)-1; a < b; a, b = a+1, b-1 {
		out[a], out[b] = out[b], out[a]
	}
	return out
}

var seed int64 = 989

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomNum(n int) []int64 {
	var out []int64
	for i := 0; i < n; i++ {
		d := nextRandom() % 10
		if i == 0 && d == 0 {
			d = 1
		}
		out = append(out, d)
	}
	return out
}

func main() {
	rounds := 1000
	nums := make([][]int64, 20)
	for i := range nums {
		nums[i] = randomNum(10000)
	}
	var digits, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			k := 1 + nextRandom()%10000
			got := addToArrayForm(nums[(r+i)%20], k)
			digits += int64(len(got))
			for j := len(got) - 6; j < len(got); j++ {
				check = (check*31 + got[j] + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 20 numbers of 10000 digits: %d digits out, checksum %d\n", rounds, digits, check)
}
