package main

import "fmt"

func main() {
	var n int64 = 3000
	var k int64 = 40000

	oval := make([]int64, n)
	onext := make([]int64, n)
	ornd := make([]int64, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		oval[i] = (state >> 16) % 1000
		if i+1 < n {
			onext[i] = i + 1
		} else {
			onext[i] = -1
		}
		state = (state*1103515245 + 12345) & 2147483647
		r := state >> 16
		if r%4 == 0 {
			ornd[i] = -1
		} else {
			ornd[i] = r % n
		}
	}

	mapp := make([]int64, n)
	nval := make([]int64, n)
	nnext := make([]int64, n)
	nrnd := make([]int64, n)

	var sink int64 = 0
	for p := int64(0); p < k; p++ {
		ii := p % n
		ornd[ii] = (p*37 + 11) % n

		for i := int64(0); i < n; i++ {
			nval[i] = oval[i]
			mapp[i] = i
		}
		for i := int64(0); i < n; i++ {
			if onext[i] == -1 {
				nnext[i] = -1
			} else {
				nnext[i] = mapp[onext[i]]
			}
			if ornd[i] == -1 {
				nrnd[i] = -1
			} else {
				nrnd[i] = mapp[ornd[i]]
			}
		}
		var checksum int64 = 0
		for i := int64(0); i < n; i++ {
			checksum += nval[i] + nnext[i]*7 + nrnd[i]*13
		}
		sink += checksum
	}
	fmt.Println(sink)
}
