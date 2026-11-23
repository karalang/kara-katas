// LeetCode #2532: Time to Cross a Bridge -- benchmark mirror of the ★ arm
// (bridge.kara): 200 cases built once, then the passes, each asking every
// case from an offset the checksum picks.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn find_crossing_time(n: i64, k: i64, time: &[Vec<i64>]) -> i64 {
    let mut left: BinaryHeap<(i64, usize)> = BinaryHeap::new();
    for i in 0..k as usize {
        left.push((time[i][0] + time[i][2], i));
    }
    let mut right: BinaryHeap<(i64, usize)> = BinaryHeap::new();
    let mut picking: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    let mut putting: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    let mut boxes = n;
    let mut now = 0;
    while boxes > 0 || !right.is_empty() || !picking.is_empty() {
        while let Some(&Reverse((done, i))) = putting.peek() {
            if done > now {
                break;
            }
            putting.pop();
            left.push((time[i][0] + time[i][2], i));
        }
        while let Some(&Reverse((done, i))) = picking.peek() {
            if done > now {
                break;
            }
            picking.pop();
            right.push((time[i][0] + time[i][2], i));
        }
        if let Some((_, i)) = right.pop() {
            now += time[i][2];
            putting.push(Reverse((now + time[i][3], i)));
        } else if boxes > 0 && !left.is_empty() {
            let (_, i) = left.pop().unwrap();
            now += time[i][0];
            boxes -= 1;
            picking.push(Reverse((now + time[i][1], i)));
        } else {
            let mut next = i64::MAX;
            if let Some(&Reverse((done, _))) = picking.peek() {
                next = next.min(done);
            }
            if boxes > 0 {
                if let Some(&Reverse((done, _))) = putting.peek() {
                    next = next.min(done);
                }
            }
            now = next;
        }
    }
    now
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2532;
    let mut cases: Vec<(i64, i64, Vec<Vec<i64>>)> = Vec::new();
    for _ in 0..200 {
        let n = next_random(&mut seed) % 1000 + 1;
        let k = next_random(&mut seed) % 100 + 1;
        let mut time = Vec::new();
        for _ in 0..k {
            let row: Vec<i64> = (0..4).map(|_| next_random(&mut seed) % 1000 + 1).collect();
            time.push(row);
        }
        cases.push((n, k, time));
    }
    let passes = 100;
    let mut check: i64 = 0;
    for p in 0..passes {
        let start = check % 200;
        for i in 0..200 {
            let (n, k, time) = &cases[((start + i) % 200) as usize];
            check = (check * 31 + find_crossing_time(*n, *k, time) + p) % 1000000007;
        }
    }
    println!("{passes} passes over 200 cases: checksum {check}");
}
