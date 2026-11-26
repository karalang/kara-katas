package main

import "fmt"

func minNumberOfFrogs(s string) int32 {
	var heard [5]int32
	var most int32
	for _, c := range s {
		var i int
		switch c {
		case 'c':
			i = 0
		case 'r':
			i = 1
		case 'o':
			i = 2
		case 'a':
			i = 3
		case 'k':
			i = 4
		default:
			return -1
		}
		heard[i]++
		if i > 0 && heard[i] > heard[i-1] {
			return -1
		}
		if heard[0]-heard[4] > most {
			most = heard[0] - heard[4]
		}
	}
	if heard[0] == heard[4] {
		return most
	}
	return -1
}

func main() {
	var seed int64 = 1419
	word := "croak"
	pool := make([]byte, 0, 500000)
	for b := 0; b < 1000; b++ {
		croaking := []int{}
		started := 0
		for started < 100 || len(croaking) > 0 {
			seed = (seed*1103515245 + 12345) % 2147483648
			r := seed / 65536
			if started < 100 && (len(croaking) == 0 || r%3 == 0) {
				pool = append(pool, 'c')
				croaking = append(croaking, 1)
				started++
			} else {
				i := int(r / 3 % int64(len(croaking)))
				pool = append(pool, word[croaking[i]])
				croaking[i]++
				if croaking[i] == 5 {
					croaking[i] = croaking[len(croaking)-1]
					croaking = croaking[:len(croaking)-1]
				}
			}
		}
	}
	text := string(pool)
	var check int64
	for w := 0; w < 500; w++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := 500 * (seed / 65536 % 801)
		check = (check*131 + int64(minNumberOfFrogs(text[start:start+100000])) + 1) % 1000000007
	}
	fmt.Printf("500 windows of 10^5 letters: checksum %d\n", check)
}
