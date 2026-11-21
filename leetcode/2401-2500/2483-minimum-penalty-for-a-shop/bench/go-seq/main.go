// LeetCode #2483: Minimum Penalty for a Shop -- bench, Go mirror of
// shop.kara.
package main

import "fmt"

func bestClosingTime(customers string) int64 {
	var balance, best, bestHour, hour int64
	for _, c := range customers {
		if c == 'Y' {
			balance++
		} else {
			balance--
		}
		hour++
		if balance > best {
			best = balance
			bestHour = hour
		}
	}
	return bestHour
}

var seed int64 = 2483

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	logs := make([][]byte, 20)
	for g := range logs {
		logs[g] = make([]byte, 10000)
		for i := range logs[g] {
			if nextRandom()%2 == 0 {
				logs[g][i] = 'Y'
			} else {
				logs[g][i] = 'N'
			}
		}
	}
	check := int64(0)
	for p := int64(0); p < 600; p++ {
		for g := 0; g < 20; g++ {
			at := check % 10000
			if logs[g][at] == 'Y' {
				logs[g][at] = 'N'
			} else {
				logs[g][at] = 'Y'
			}
			log := string(logs[g])
			check = (check*31 + bestClosingTime(log) + p) % 1000000007
		}
	}
	fmt.Printf("600 passes over 20 logs of 10^4 hours: checksum %d\n", check)
}
