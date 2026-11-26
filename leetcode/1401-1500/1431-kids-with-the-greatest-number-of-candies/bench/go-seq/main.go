package main

import "fmt"

func kidsWithCandies(candies []int32, extraCandies int32) []bool {
	most := candies[0]
	for _, c := range candies[1:] {
		if c > most {
			most = c
		}
	}
	answer := make([]bool, len(candies))
	for i, c := range candies {
		answer[i] = c+extraCandies >= most
	}
	return answer
}

func main() {
	var seed int64 = 1431
	pool := make([]int32, 1000000)
	for i := range pool {
		seed = (seed*1103515245 + 12345) % 2147483648
		pool[i] = int32(1 + seed/65536%100)
	}
	var check int64
	for w := 0; w < 1000000; w++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := seed / 65536 % 999901
		seed = (seed*1103515245 + 12345) % 2147483648
		extra := int32(1 + seed/65536%50)
		var bits int64
		for j, b := range kidsWithCandies(pool[start:start+100], extra) {
			if b {
				bits += int64(j) + 1
			}
		}
		check = (check*131 + bits) % 1000000007
	}
	fmt.Printf("10^6 windows of 100 kids: checksum %d\n", check)
}
