// LeetCode #1736: Latest Time by Replacing Hidden Digits -- the bench
// (time.kara): each hidden digit the largest its neighbours allow.
package main

import "fmt"

func maximumTime(time string) string {
	t := []rune(time)
	if t[0] == '?' {
		if t[1] == '?' || t[1] <= '3' {
			t[0] = '2'
		} else {
			t[0] = '1'
		}
	}
	if t[1] == '?' {
		if t[0] == '2' {
			t[1] = '3'
		} else {
			t[1] = '9'
		}
	}
	if t[3] == '?' {
		t[3] = '5'
	}
	if t[4] == '?' {
		t[4] = '9'
	}
	return string(t)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 1000000
	var rounds int64 = 10
	var seed int64 = 1736
	times := make([]string, 0, count)
	for i := 0; i < count; i++ {
		t := nextRandom(&seed) % 1440
		shown := fmt.Sprintf("%d%d:%d%d", t/60/10, t/60%10, t%60/10, t%60%10)
		hidden := make([]rune, 0, 5)
		for _, c := range shown {
			if c != ':' && nextRandom(&seed)%2 == 0 {
				hidden = append(hidden, '?')
			} else {
				hidden = append(hidden, c)
			}
		}
		times = append(times, string(hidden))
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, time := range times {
			b := maximumTime(time)
			sum += int64(b[1]) - 48
			check = (check*31 + int64(b[0])*1000 + int64(b[1])*100 + int64(b[3])*10 + int64(b[4]) + r) % 1000000007
		}
	}
	fmt.Printf("%d times, %d rounds: hour digits sum to %d, checksum %d\n", count, rounds, sum, check)
}
