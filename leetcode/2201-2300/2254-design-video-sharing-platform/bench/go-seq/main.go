// LeetCode #2254: Design Video Sharing Platform -- the benchmark's Go
// mirror of videos.kara: the videos in a slice indexed by id (nil once
// removed) and the freed ids in a binary min-heap, smallest first.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

type video struct {
	content                string
	views, likes, dislikes int64
}

type platform struct {
	slots []*video
	free  []int64
}

func (p *platform) push(id int64) {
	p.free = append(p.free, id)
	at := len(p.free) - 1
	for at > 0 && p.free[(at-1)/2] > p.free[at] {
		p.free[at], p.free[(at-1)/2] = p.free[(at-1)/2], p.free[at]
		at = (at - 1) / 2
	}
}

func (p *platform) pop() int64 {
	top := p.free[0]
	last := len(p.free) - 1
	p.free[0] = p.free[last]
	p.free = p.free[:last]
	at := 0
	for {
		least := at
		for _, child := range [2]int{2*at + 1, 2*at + 2} {
			if child < len(p.free) && p.free[child] < p.free[least] {
				least = child
			}
		}
		if least == at {
			break
		}
		p.free[at], p.free[least] = p.free[least], p.free[at]
		at = least
	}
	return top
}

func (p *platform) get(id int64) *video {
	if id < int64(len(p.slots)) {
		return p.slots[id]
	}
	return nil
}

func (p *platform) upload(content string) int64 {
	held := &video{content: content}
	if len(p.free) > 0 {
		id := p.pop()
		p.slots[id] = held
		return id
	}
	p.slots = append(p.slots, held)
	return int64(len(p.slots)) - 1
}

func (p *platform) remove(id int64) {
	if p.get(id) != nil {
		p.slots[id] = nil
		p.push(id)
	}
}

func (p *platform) watch(id, start, end int64) string {
	v := p.get(id)
	if v == nil {
		return "-1"
	}
	v.views++
	last := end
	if l := int64(len(v.content)) - 1; l < last {
		last = l
	}
	return v.content[start : last+1]
}

type call struct {
	kind int64
	args []int64
	text string
}

func run(calls []call) []string {
	p := &platform{}
	var answers []string
	for _, c := range calls {
		switch c.kind {
		case 0:
			answers = append(answers, strconv.FormatInt(p.upload(c.text), 10))
		case 1:
			p.remove(c.args[0])
		case 2:
			answers = append(answers, p.watch(c.args[0], c.args[1], c.args[2]))
		case 3:
			if v := p.get(c.args[0]); v != nil {
				v.likes++
			}
		case 4:
			if v := p.get(c.args[0]); v != nil {
				v.dislikes++
			}
		case 5:
			if v := p.get(c.args[0]); v != nil {
				answers = append(answers, fmt.Sprintf("[%d, %d]", v.likes, v.dislikes))
			} else {
				answers = append(answers, "[-1]")
			}
		default:
			views := int64(-1)
			if v := p.get(c.args[0]); v != nil {
				views = v.views
			}
			answers = append(answers, strconv.FormatInt(views, 10))
		}
	}
	return answers
}

var seed int64 = 2254

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func callsOf(count, longest int64) []call {
	calls := make([]call, 0, count)
	var uploads int64
	for i := int64(0); i < count; i++ {
		pick := nextRandom() % 10
		id := nextRandom() % (uploads + 2)
		if pick < 3 {
			length := nextRandom()%(longest-2) + 3
			var b strings.Builder
			for k := int64(0); k < length; k++ {
				b.WriteByte(byte('0' + nextRandom()%10))
			}
			calls = append(calls, call{0, nil, b.String()})
			uploads++
		} else if pick == 3 {
			calls = append(calls, call{1, []int64{id}, ""})
		} else if pick < 6 {
			start := nextRandom() % 3
			end := start + nextRandom()%8 + 1
			calls = append(calls, call{2, []int64{id, start, end}, ""})
		} else {
			calls = append(calls, call{pick - 3, []int64{id}, ""})
		}
	}
	return calls
}

func tally(answers []string, check int64) int64 {
	c := check
	for _, a := range answers {
		for i := 0; i < len(a); i++ {
			c = (c*131 + int64(a[i])) % 1000000007
		}
		c = (c*131 + 1) % 1000000007
	}
	return c
}

func main() {
	var answered, check int64
	for t := 0; t < 120; t++ {
		answers := run(callsOf(25000, 8))
		answered += int64(len(answers))
		check = tally(answers, check)
	}
	fmt.Printf("120 platforms of 25000 calls: %d answers, checksum %d\n", answered, check)
}
