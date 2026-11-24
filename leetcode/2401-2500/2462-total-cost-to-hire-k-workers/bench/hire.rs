// LeetCode #2462: Total Cost to Hire K Workers -- the bench, the ★ arm in
// Rust: two `BinaryHeap`s of `Reverse((cost, index))`, the first and the
// last `candidates` workers, each session taking the cheaper top and
// refilling its heap from the untaken middle.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn total_cost(costs: &[i64], k: i64, candidates: i64) -> i64 {
    let n = costs.len() as i64;
    let mut front = BinaryHeap::new();
    let mut back = BinaryHeap::new();
    let mut next = 0i64;
    let mut last = n - 1;
    while next < candidates && next <= last {
        front.push(Reverse((costs[next as usize], next)));
        next += 1;
    }
    while n - 1 - last < candidates && next <= last {
        back.push(Reverse((costs[last as usize], last)));
        last -= 1;
    }
    let mut total = 0;
    for _ in 0..k {
        let take_front = match (front.peek(), back.peek()) {
            (Some(Reverse(f)), Some(Reverse(b))) => f <= b,
            (Some(_), None) => true,
            _ => false,
        };
        if take_front {
            let Reverse((cost, _)) = front.pop().unwrap();
            total += cost;
            if next <= last {
                front.push(Reverse((costs[next as usize], next)));
                next += 1;
            }
        } else {
            let Reverse((cost, _)) = back.pop().unwrap();
            total += cost;
            if next <= last {
                back.push(Reverse((costs[last as usize], last)));
                last -= 1;
            }
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    // 10 lists of 10^5 costs from 1 to 10^5 built once; then 32 passes,
    // each setting one cost of every list from the checksum so far, then
    // answering every list with k of 5 10^4 and 1 + 97 p candidates,
    // folding the answer plus the pass into the checksum
    let mut seed = 2462;
    let mut lists: Vec<Vec<i64>> = (0..10).map(|_| (0..100000).map(|_| 1 + wide_random(&mut seed) % 100000).collect()).collect();
    let mut check = 0i64;
    for p in 0..32i64 {
        let candidates = 1 + 97 * p;
        for a in 0..lists.len() {
            lists[a][((check + a as i64) % 100000) as usize] = 1 + check % 100000;
            check = (check * 31 + total_cost(&lists[a], 50000, candidates) + p) % 1000000007;
        }
    }
    println!("32 passes over 10 lists of 10^5: checksum {check}");
}
