// LeetCode #2177: Find Three Consecutive Integers That Sum to a Given
// Number -- the benchmark's Go mirror of three.kara.
package main

import "fmt"

func sumOfThree(num int64) []int64 {
	if num%3 != 0 {
		return []int64{}
	}
	x := num / 3
	return []int64{x - 1, x, x + 1}
}

var seed int64 = 2177

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	row := make([]int64, 0, 1000000)
	for i := 0; i < 1000000; i++ {
		a := nextRandom()
		b := nextRandom()
		c := nextRandom()
		row = append(row, ((a*32768+b)*32768+c)%1000000000000001)
	}
	var found, check int64
	for pass := int64(0); pass < 2; pass++ {
		for _, num := range row {
			three := sumOfThree(num + pass)
			if len(three) == 3 {
				found++
				check = (check*31 + three[2]%1000000007) % 1000000007
			}
		}
	}
	fmt.Printf("2000000 solves: %d found, checksum %d\n", found, check)
}
