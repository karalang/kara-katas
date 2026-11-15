// LeetCode #1585 bench: the same first-unused-copy match, in Go. Each
// digit's queue is a slice taken from the front.
package main

import (
	"fmt"
	"slices"
)

func isTransformable(s, t string) bool {
	var at [10][]int64
	for i := 0; i < len(s); i++ {
		d := s[i] - '0'
		at[d] = append(at[d], int64(i))
	}
	for i := 0; i < len(t); i++ {
		d := int(t[i] - '0')
		if len(at[d]) == 0 {
			return false
		}
		p := at[d][0]
		at[d] = at[d][1:]
		for e := 0; e < d; e++ {
			if len(at[e]) > 0 && at[e][0] < p {
				return false
			}
		}
	}
	return true
}

var seed int64 = 1585

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 100000
	type problem struct{ s, t string }
	problems := make([]problem, 0, 40)
	for k := 0; k < 40; k++ {
		s := make([]byte, 0, n)
		for i := 0; i < n; i++ {
			s = append(s, byte('0'+nextRandom()%10))
		}
		t := slices.Clone(s)
		for r := 0; r < 2000; r++ {
			a := (nextRandom()*32768 + nextRandom()) % (n - 50)
			b := a + nextRandom()%50 + 1
			slices.Sort(t[a:b])
		}
		if k%2 == 1 {
			a := (nextRandom()*32768 + nextRandom()) % n
			b := (nextRandom()*32768 + nextRandom()) % n
			t[a], t[b] = t[b], t[a]
		}
		problems = append(problems, problem{string(s), string(t)})
	}
	var check, yes int64
	for _, pr := range problems {
		ok := isTransformable(pr.s, pr.t)
		if ok {
			yes++
		}
		v := int64(0)
		if ok {
			v = 1
		}
		check = mix(check, v)
	}
	fmt.Printf("40 problems of 100000 digits: %d transformable, checksum %d\n", yes, check)
}
