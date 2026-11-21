// LeetCode #2402: Meeting Rooms III -- the bench, the ★ arm in Rust: a
// `BinaryHeap` of free rooms and one of (end, room) for the rooms in use,
// both reversed to pop the smallest, over the meetings sorted by start.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn most_booked(n: usize, meetings: &[(i64, i64)]) -> usize {
    let mut order = meetings.to_vec();
    order.sort();
    let mut free: BinaryHeap<Reverse<usize>> = (0..n).map(Reverse).collect();
    let mut busy: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    let mut count = vec![0i64; n];
    for &(start, end) in &order {
        while let Some(&Reverse((at, room))) = busy.peek() {
            if at > start {
                break;
            }
            busy.pop();
            free.push(Reverse(room));
        }
        if let Some(Reverse(room)) = free.pop() {
            count[room] += 1;
            busy.push(Reverse((end, room)));
        } else {
            let Reverse((at, room)) = busy.pop().unwrap();
            count[room] += 1;
            busy.push(Reverse((at + end - start, room)));
        }
    }
    let mut best = 0;
    for room in 1..n {
        if count[room] > count[best] {
            best = room;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2402;
    let mut cases: Vec<Vec<(i64, i64)>> = Vec::new();
    for c in 0..10i64 {
        let mut starts: Vec<i64> = (0..500000).collect();
        for i in 0..100000usize {
            let hi = next_random(&mut seed);
            let j = i + ((hi * 32768 + next_random(&mut seed)) % (500000 - i as i64)) as usize;
            starts.swap(i, j);
        }
        let meetings = (0..100000).map(|i| (starts[i], starts[i] + 1 + next_random(&mut seed) % (1 + 500 * c))).collect();
        cases.push(meetings);
    }
    let mut check: i64 = 0;
    for p in 0..10 {
        for meetings in &cases {
            check = (check * 31 + most_booked(100, meetings) as i64 + p) % 1000000007;
        }
    }
    println!("10 passes over 10 cases of 10^5 meetings in 100 rooms: checksum {}", check);
}
