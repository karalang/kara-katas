// LeetCode #2381: Shifting Letters II -- the bench, the ★ arm in Go: a
// difference array of the shifts, its running sum each letter's step.
package main

import "fmt"

func shiftingLetters(s string, shifts [][3]int64) string {
	n := len(s)
	diff := make([]int64, n+1)
	for _, shift := range shifts {
		step := int64(-1)
		if shift[2] == 1 {
			step = 1
		}
		diff[shift[0]] += step
		diff[shift[1]+1] -= step
	}
	out := make([]byte, 0)
	total := int64(0)
	for i := 0; i < n; i++ {
		total += diff[i]
		letter := (int64(s[i]-'a') + total) % 26
		if letter < 0 {
			letter += 26
		}
		out = append(out, byte('a'+letter))
	}
	return string(out)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// a string of 5 * 10^4 letters and 10 lists of 5 * 10^4 shifts, list
	// l's shifts up to 10^l letters long, capped at the string; pass p
	// applies list p % 10
	seed := int64(2381)
	n := int64(50000)
	letters := make([]byte, n)
	for i := range letters {
		letters[i] = byte('a' + nextRandom(&seed)%26)
	}
	s := string(letters)
	lists := make([][][3]int64, 0, 10)
	for l := 0; l < 10; l++ {
		reach := int64(1)
		for k := 0; k < l; k++ {
			reach = min(reach*10, n)
		}
		list := make([][3]int64, 0, n)
		for i := int64(0); i < n; i++ {
			start := nextRandom(&seed) % n
			end := min(start+nextRandom(&seed)%reach, n-1)
			list = append(list, [3]int64{start, end, nextRandom(&seed) % 2})
		}
		lists = append(lists, list)
	}
	check := int64(0)
	for p := int64(0); p < 200; p++ {
		t := shiftingLetters(s, lists[p%10])
		for i := 0; i < len(t); i++ {
			check = (check*31 + int64(t[i]-'a') + p) % 1000000007
		}
	}
	fmt.Printf("200 passes over 5 * 10^4 letters: checksum %d\n", check)
}
