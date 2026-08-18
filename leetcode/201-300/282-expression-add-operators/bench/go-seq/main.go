// LeetCode 282 bench mirror — Go. Same search, same string building.
package main

import "fmt"

const Inputs = 220
const NDig = 9

var num []byte
var target, found, hash int64

func search(pos int, expr string, cur, last int64) {
	if pos == NDig {
		if cur == target {
			found++
			hash = (hash*31 + int64(len(expr))) % 1000000007
		}
		return
	}
	for end := pos + 1; end <= NDig; end++ {
		if end > pos+1 && num[pos] == '0' {
			return
		}
		var n int64
		for k := pos; k < end; k++ {
			n = n*10 + int64(num[k]-'0')
		}
		piece := string(num[pos:end])
		if pos == 0 {
			search(end, piece, n, n)
		} else {
			search(end, expr+"+"+piece, cur+n, n)
			search(end, expr+"-"+piece, cur-n, -n)
			search(end, expr+"*"+piece, cur-last+last*n, last*n)
		}
	}
}

func main() {
	seed := int64(20260820)
	num = make([]byte, NDig)
	var total int64
	for t := 0; t < Inputs; t++ {
		for d := 0; d < NDig; d++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			num[d] = byte('0' + 1 + (seed/19)%6)
		}
		seed = (seed*1103515245 + 12345) % 2147483648
		target = (seed / 23) % 40
		found = 0
		search(0, "", 0, 0)
		total += found
	}
	fmt.Println(total, hash)
}
