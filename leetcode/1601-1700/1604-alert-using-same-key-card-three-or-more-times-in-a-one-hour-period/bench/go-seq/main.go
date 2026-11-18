// LeetCode #1604: Alert Using Same Key-Card Three or More Times in a One
// Hour Period -- the bench in Go, mirroring alert.kara: each name's
// minutes in a map, the names sorted (Go has no ordered map), each list
// sorted.
package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

var names8 = []string{"daniel", "luis", "alice", "bob", "john", "leslie", "clare", "anna"}

func minutes(t string) int32 {
	h, m, _ := strings.Cut(t, ":")
	hv, _ := strconv.Atoi(h)
	mv, _ := strconv.Atoi(m)
	return int32(hv*60 + mv)
}

func alertNames(keyName, keyTime []string) []string {
	uses := map[string][]int32{}
	for i, name := range keyName {
		uses[name] = append(uses[name], minutes(keyTime[i]))
	}
	keys := make([]string, 0, len(uses))
	for k := range uses {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	var out []string
	for _, name := range keys {
		times := uses[name]
		sort.Slice(times, func(a, b int) bool { return times[a] < times[b] })
		for i := 2; i < len(times); i++ {
			if times[i]-times[i-2] <= 60 {
				out = append(out, name)
				break
			}
		}
	}
	return out
}

var seed int64 = 1604

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	type day struct{ names, times []string }
	var days []day
	for d := 0; d < 30; d++ {
		var dd day
		for k := 0; k < 100000; k++ {
			who := big() % 20000
			if who < 8 {
				dd.names = append(dd.names, names8[who])
			} else {
				dd.names = append(dd.names, fmt.Sprintf("%s%d", names8[who%8], who/8))
			}
			t := big() % 1440
			dd.times = append(dd.times, fmt.Sprintf("%02d:%02d", t/60, t%60))
		}
		days = append(days, dd)
	}
	var check, alerts int64
	for _, d := range days {
		for _, name := range alertNames(d.names, d.times) {
			alerts++
			for _, b := range []byte(name) {
				check = mix(check, int64(b))
			}
			check = mix(check, 0)
		}
	}
	fmt.Printf("30 days of 100000 swipes by 20000 names: %d alerts, checksum %d\n", alerts, check)
}
