// LeetCode #1103: Distribute Candies to People -- the bench in Go: the ★
// arm (gifts of 1, 2, 3, ... in turn, the last whatever is left) over 64
// problems, each round moving every problem's candies.
package main

import "fmt"

func distributeCandies(candies, numPeople int64) []int64 {
	people := make([]int64, numPeople)
	left, gift := candies, int64(1)
	for left > 0 {
		given := gift
		if left < given {
			given = left
		}
		people[(gift-1)%numPeople] += given
		left -= given
		gift++
	}
	return people
}

var seed int64 = 1103

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type problem struct{ candies, n int64 }
	problems := make([]problem, 0, 64)
	for j := 0; j < 64; j++ {
		hi := nextRandom()
		candies := (hi*32768+nextRandom())%1000000000 + 1
		n := nextRandom()%1000 + 1
		problems = append(problems, problem{candies, n})
	}
	var total, check int64
	for round := int64(0); round < 200; round++ {
		for j := range problems {
			candies := (problems[j].candies+round*7919+int64(j)*104729)%1000000000 + 1
			problems[j].candies = candies
			n := problems[j].n
			people := distributeCandies(candies, n)
			total += people[0] + people[n-1]
			for _, c := range people {
				check = (check*31 + c + 1) % 1000000007
			}
		}
	}
	fmt.Printf("200 rounds over 64 problems of up to 10^9 candies: first and last people hold %d, checksum %d\n", total, check)
}
