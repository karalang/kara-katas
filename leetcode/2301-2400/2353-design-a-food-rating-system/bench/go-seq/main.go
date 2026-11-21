// LeetCode #2353: Design a Food Rating System -- the bench, the ★ arm: lazy
// heaps, a map from each food to its rating and its cuisine, and for each
// cuisine a min-first binary heap of (-rating, food) holding every key a
// food was ever given; a query pops the tops that are no longer true.
package main

import "fmt"

type entry struct {
	negated int64
	food    string
}

func less(a, b entry) bool {
	return a.negated < b.negated || a.negated == b.negated && a.food < b.food
}

type heap []entry

func (h *heap) push(e entry) {
	*h = append(*h, e)
	s := *h
	i := len(s) - 1
	for i > 0 {
		up := (i - 1) / 2
		if !less(s[i], s[up]) {
			break
		}
		s[i], s[up] = s[up], s[i]
		i = up
	}
}

func (h *heap) pop() {
	s := *h
	last := len(s) - 1
	s[0] = s[last]
	s = s[:last]
	i := 0
	for {
		l, r, m := 2*i+1, 2*i+2, i
		if l < len(s) && less(s[l], s[m]) {
			m = l
		}
		if r < len(s) && less(s[r], s[m]) {
			m = r
		}
		if m == i {
			break
		}
		s[i], s[m] = s[m], s[i]
		i = m
	}
	*h = s
}

type foodRatings struct {
	rating    map[string]int64
	cuisineOf map[string]string
	heaps     map[string]*heap
}

func newFoodRatings(foods, cuisines []string, ratings []int64) *foodRatings {
	t := &foodRatings{map[string]int64{}, map[string]string{}, map[string]*heap{}}
	for i := range foods {
		t.rating[foods[i]] = ratings[i]
		t.cuisineOf[foods[i]] = cuisines[i]
		h, ok := t.heaps[cuisines[i]]
		if !ok {
			h = &heap{}
			t.heaps[cuisines[i]] = h
		}
		h.push(entry{-ratings[i], foods[i]})
	}
	return t
}

func (t *foodRatings) changeRating(food string, newRating int64) {
	t.rating[food] = newRating
	t.heaps[t.cuisineOf[food]].push(entry{-newRating, food})
}

func (t *foodRatings) highestRated(cuisine string) string {
	h := t.heaps[cuisine]
	for {
		top := (*h)[0]
		if t.rating[top.food] == -top.negated {
			return top.food
		}
		h.pop()
	}
}

var seed int64 = 2353

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func fourLetters(v int64) string {
	return string([]byte{byte(97 + v/17576), byte(97 + v/676%26), byte(97 + v/26%26), byte(97 + v%26)})
}

type call struct {
	kind   int64
	name   string
	rating int64
}

func main() {
	const n = 10000
	foods := make([]string, n)
	for i := int64(0); i < n; i++ {
		foods[i] = fourLetters(i * 7919 % 456976)
	}
	cuisines := make([]string, n)
	for i := range cuisines {
		cuisines[i] = fmt.Sprintf("c%d", nextRandom()%100)
	}
	ratings := make([]int64, n)
	for i := range ratings {
		ratings[i] = 1 + nextRandom()%100000000
	}
	calls := make([]call, 0, 100000)
	for i := 0; i < 100000; i++ {
		f := nextRandom() % n
		if i%3 == 2 {
			calls = append(calls, call{1, cuisines[f], 0})
		} else {
			calls = append(calls, call{0, foods[f], 1 + nextRandom()%100000000})
		}
	}
	check := int64(0)
	for p := int64(0); p < 100; p++ {
		t := newFoodRatings(foods, cuisines, ratings)
		for _, c := range calls {
			if c.kind == 0 {
				t.changeRating(c.name, c.rating)
			} else {
				for _, b := range []byte(t.highestRated(c.name)) {
					check = (check*31 + int64(b)) % 1000000007
				}
				check = (check*31 + p) % 1000000007
			}
		}
	}
	fmt.Printf("100 passes over 10^4 foods and 10^5 calls: checksum %d\n", check)
}
