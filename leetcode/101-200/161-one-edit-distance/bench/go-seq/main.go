package main

import "fmt"

func tailsEqual(s, l []int64, ss, se, ls, le int64) bool {
	a := ss
	b := ls
	for a < se && b < le {
		if s[a] != l[b] {
			return false
		}
		a++
		b++
	}
	return a == se && b == le
}

func check(s []int64, so, m int64, l []int64, lo, n int64) bool {
	if n-m > 1 {
		return false
	}
	for i := int64(0); i < m; i++ {
		if s[so+i] != l[lo+i] {
			if m == n {
				return tailsEqual(s, l, so+i+1, so+m, lo+i+1, lo+n)
			}
			return tailsEqual(s, l, so+i, so+m, lo+i+1, lo+n)
		}
	}
	return n-m == 1
}

func isOneEdit(a []int64, oa, la int64, b []int64, ob, lb int64) bool {
	if la <= lb {
		return check(a, oa, la, b, ob, lb)
	}
	return check(b, ob, lb, a, oa, la)
}

func main() {
	var pairs int64 = 4000
	var l int64 = 48
	var reps int64 = 3000
	stride := l + 2
	cap := pairs * stride

	bufA := make([]int64, cap)
	bufB := make([]int64, cap)
	lenA := make([]int64, pairs)
	lenB := make([]int64, pairs)

	var state int64 = 12345
	for pi := int64(0); pi < pairs; pi++ {
		oa := pi * stride
		ob := pi * stride
		for k := int64(0); k < l; k++ {
			state = (state*1103515245 + 12345) & 2147483647
			bufA[oa+k] = state % 26
		}
		lenA[pi] = l
		state = (state*1103515245 + 12345) & 2147483647
		kind := state % 4
		if kind == 0 {
			for j := int64(0); j < l; j++ {
				bufB[ob+j] = bufA[oa+j]
			}
			state = (state*1103515245 + 12345) & 2147483647
			pos := state % l
			bufB[ob+pos] = (bufA[oa+pos] + 1) % 26
			lenB[pi] = l
		} else if kind == 1 {
			state = (state*1103515245 + 12345) & 2147483647
			pos := state % (l + 1)
			for j := int64(0); j < pos; j++ {
				bufB[ob+j] = bufA[oa+j]
			}
			state = (state*1103515245 + 12345) & 2147483647
			bufB[ob+pos] = state % 26
			for t := pos; t < l; t++ {
				bufB[ob+t+1] = bufA[oa+t]
			}
			lenB[pi] = l + 1
		} else if kind == 2 {
			state = (state*1103515245 + 12345) & 2147483647
			pos := state % l
			var w int64 = 0
			for j := int64(0); j < l; j++ {
				if j != pos {
					bufB[ob+w] = bufA[oa+j]
					w++
				}
			}
			lenB[pi] = l - 1
		} else {
			for j := int64(0); j < l; j++ {
				bufB[ob+j] = bufA[oa+j]
			}
			state = (state*1103515245 + 12345) & 2147483647
			p1 := state % l
			state = (state*1103515245 + 12345) & 2147483647
			p2 := (p1 + 1 + state%(l-1)) % l
			bufB[ob+p1] = (bufA[oa+p1] + 1) % 26
			bufB[ob+p2] = (bufA[oa+p2] + 1) % 26
			lenB[pi] = l
		}
	}

	var sink int64 = 0
	for rep := int64(0); rep < reps; rep++ {
		idx := rep % pairs
		col := (rep*7 + 3) % l
		oa := idx * stride
		bufA[oa+col] = (bufA[oa+col] + 1) % 26
		for i := int64(0); i < pairs; i++ {
			o := i * stride
			if isOneEdit(bufA, o, lenA[i], bufB, o, lenB[i]) {
				sink++
			}
		}
	}
	fmt.Println(sink)
}
