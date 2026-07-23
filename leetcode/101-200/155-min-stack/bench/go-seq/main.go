package main

import "fmt"

type MinStack struct {
	data []int64
	mins []int64
}

func msNew() *MinStack {
	return &MinStack{data: []int64{}, mins: []int64{}}
}

func msPush(st *MinStack, x int64) {
	st.data = append(st.data, x)
	m := len(st.mins)
	if m == 0 || x <= st.mins[m-1] {
		st.mins = append(st.mins, x)
	} else {
		st.mins = append(st.mins, st.mins[m-1])
	}
}

func msPop(st *MinStack) {
	st.data = st.data[:len(st.data)-1]
	st.mins = st.mins[:len(st.mins)-1]
}

func msTop(st *MinStack) int64 {
	return st.data[len(st.data)-1]
}

func msGetMin(st *MinStack) int64 {
	return st.mins[len(st.mins)-1]
}

func main() {
	var ops int64 = 90000000
	var cap int64 = 100000

	st := msNew()
	var state int64 = 12345
	var sz int64 = 0
	var sink int64 = 0

	for i := int64(0); i < ops; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		op := (state / 1024) % 4
		if sz == 0 {
			state = (state*1103515245 + 12345) & 2147483647
			val := state%2000000 - 1000000
			msPush(st, val)
			sz++
		} else if sz >= cap {
			msPop(st)
			sz--
		} else if op == 0 {
			state = (state*1103515245 + 12345) & 2147483647
			val := state%2000000 - 1000000
			msPush(st, val)
			sz++
		} else if op == 1 {
			msPop(st)
			sz--
		} else if op == 2 {
			sink += msGetMin(st)
		} else {
			sink += msTop(st)
		}
	}
	fmt.Println(sink)
}
