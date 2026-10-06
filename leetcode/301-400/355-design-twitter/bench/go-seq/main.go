// Bench for LeetCode #355 -- Go mirror of twitter.kara (the starred arm):
// per-user tweet lists merged newest-first through a priority queue.
package main

import (
	"container/heap"
	"fmt"
)

const (
	users   = 1000
	posts   = 300000
	follows = 100000
	feeds   = 300000
)

type tweet struct{ time, id int64 }

type candidate struct{ time, tweet, author, index int64 }

// candidates is a max-heap ordered like the Kāra arm's derived Ord: by time,
// then tweet, author and index.
type candidates []candidate

func (c candidates) Len() int { return len(c) }
func (c candidates) Less(i, j int) bool {
	a, b := c[i], c[j]
	if a.time != b.time {
		return a.time > b.time
	}
	if a.tweet != b.tweet {
		return a.tweet > b.tweet
	}
	if a.author != b.author {
		return a.author > b.author
	}
	return a.index > b.index
}
func (c candidates) Swap(i, j int) { c[i], c[j] = c[j], c[i] }
func (c *candidates) Push(x any)   { *c = append(*c, x.(candidate)) }
func (c *candidates) Pop() any {
	old := *c
	n := len(old)
	x := old[n-1]
	*c = old[:n-1]
	return x
}

type twitter struct {
	clock   int64
	tweets  map[int64][]tweet
	follows map[int64]map[int64]struct{}
}

func newTwitter() *twitter {
	return &twitter{tweets: map[int64][]tweet{}, follows: map[int64]map[int64]struct{}{}}
}

func (t *twitter) postTweet(user, id int64) {
	t.clock++
	t.tweets[user] = append(t.tweets[user], tweet{t.clock, id})
}

func (t *twitter) newsFeed(user int64) []int64 {
	authors := []int64{user}
	for f := range t.follows[user] {
		if f != user {
			authors = append(authors, f)
		}
	}
	queue := &candidates{}
	for _, a := range authors {
		list := t.tweets[a]
		if len(list) > 0 {
			last := int64(len(list) - 1)
			heap.Push(queue, candidate{list[last].time, list[last].id, a, last})
		}
	}
	feed := make([]int64, 0, 10)
	for len(feed) < 10 && queue.Len() > 0 {
		c := heap.Pop(queue).(candidate)
		feed = append(feed, c.tweet)
		if c.index > 0 {
			older := t.tweets[c.author][c.index-1]
			heap.Push(queue, candidate{older.time, older.id, c.author, c.index - 1})
		}
	}
	return feed
}

func (t *twitter) follow(follower, followee int64) {
	set, ok := t.follows[follower]
	if !ok {
		set = map[int64]struct{}{}
		t.follows[follower] = set
	}
	set[followee] = struct{}{}
}

func main() {
	t := newTwitter()
	var seed int64 = 355
	for i := int64(0); i < posts; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		t.postTweet(seed%users, i)
	}
	for i := 0; i < follows; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		a := seed % users
		seed = (seed*1103515245 + 12345) % 2147483648
		t.follow(a, seed%users)
	}
	var sink int64
	for i := 0; i < feeds; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		for _, id := range t.newsFeed(seed % users) {
			sink = (sink*31 + id) % 1000000007
		}
	}
	fmt.Println(sink)
}
