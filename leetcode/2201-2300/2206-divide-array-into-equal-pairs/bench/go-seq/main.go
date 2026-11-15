// benchmark's Go mirror of pairs.kara (LeetCode #2206, the ★ arm): a count
// per value up to 500, then one pass over the counts.
package main

import "fmt"

func divideArray(nums []int64) bool {
	count := make([]int64, 501)
	for _, x := range nums {
		count[x]++
	}
	for _, c := range count {
		if c%2 == 1 {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

// 1000 numbers up to `top`: 500 pairs shuffled, or 1000 drawn freely
func randomArray(paired bool, top int64, seed *int64) []int64 {
	nums := []int64{}
	if paired {
		for i := 0; i < 500; i++ {
			x := nextRandom(seed)%top + 1
			nums = append(nums, x, x)
		}
		for i := int64(999); i >= 1; i-- {
			j := nextRandom(seed) % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
	} else {
		for i := 0; i < 1000; i++ {
			nums = append(nums, nextRandom(seed)%top+1)
		}
	}
	return nums
}

func main() {
	seed := int64(2206)
	tops := []int64{2, 5, 500}
	arrays := [][]int64{}
	for a := 0; a < 200; a++ {
		arrays = append(arrays, randomArray(a%4 != 3, tops[a%3], &seed))
	}
	// each odd pass punches one number of every array before the count and
	// puts it back after
	check := int64(0)
	for p := int64(0); p < 1500; p++ {
		for a := int64(0); a < 200; a++ {
			at := (p*7 + a) % 1000
			old := arrays[a][at]
			if p%2 == 1 {
				arrays[a][at] = (p+a)%500 + 1
			}
			paired := divideArray(arrays[a])
			arrays[a][at] = old
			v := int64(1)
			if paired {
				v = 2
			}
			check = (check*31 + v) % 1000000007
		}
	}
	fmt.Printf("1500 passes over 200 arrays: checksum %d\n", check)
}
