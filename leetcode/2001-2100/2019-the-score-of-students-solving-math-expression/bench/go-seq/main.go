// LeetCode #2019: The Score of Students Solving Math Expression -- the ★ arm's
// benchmark, a mirror of score.kara: each run's values in a map used as a set.
package main

import "fmt"

func scoreOfStudents(s string, answers []int64) int64 {
	n := (len(s) + 1) / 2
	digits := make([]int64, n)
	for i := 0; i < n; i++ {
		digits[i] = int64(s[2*i] - '0')
	}
	var sum int64
	product := digits[0]
	for i := 0; i < n-1; i++ {
		if s[2*i+1] == '+' {
			sum += product
			product = digits[i+1]
		} else {
			product *= digits[i+1]
		}
	}
	correct := sum + product
	values := make([][]map[int64]struct{}, n)
	for i := range values {
		values[i] = make([]map[int64]struct{}, n)
		for j := range values[i] {
			values[i][j] = map[int64]struct{}{}
		}
		values[i][i][digits[i]] = struct{}{}
	}
	for length := 2; length <= n; length++ {
		for i := 0; i+length-1 < n; i++ {
			j := i + length - 1
			cell := map[int64]struct{}{}
			for k := i; k < j; k++ {
				plus := s[2*k+1] == '+'
				for a := range values[i][k] {
					for b := range values[k+1][j] {
						var v int64
						if plus {
							v = a + b
						} else {
							v = a * b
						}
						if v <= 1000 {
							cell[v] = struct{}{}
						}
					}
				}
			}
			values[i][j] = cell
		}
	}
	var points int64
	for _, answer := range answers {
		if answer == correct {
			points += 5
		} else if _, ok := values[0][n-1][answer]; ok {
			points += 2
		}
	}
	return points
}

var seed int64 = 2019

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	expressions := []string{}
	answerLists := [][]int64{}
	for e := int64(0); e < 200; e++ {
		top := e%9 + 1
		times := e%7 + 2
		b := []byte{}
		for i := 0; i < 16; i++ {
			if i > 0 {
				if nextRandom()%10 < times {
					b = append(b, '*')
				} else {
					b = append(b, '+')
				}
			}
			b = append(b, byte('0'+nextRandom()%(top+1)))
		}
		expressions = append(expressions, string(b))
		answers := make([]int64, 2000)
		for i := range answers {
			answers[i] = nextRandom() % 1001
		}
		answerLists = append(answerLists, answers)
	}
	var calls, total, check int64
	for r := 0; r < 10; r++ {
		for e := range expressions {
			points := scoreOfStudents(expressions[e], answerLists[e])
			calls++
			total += points
			check = (check*31 + points) % 1000000007
		}
	}
	fmt.Printf("%d calls: %d points, checksum %d\n", calls, total, check)
}
