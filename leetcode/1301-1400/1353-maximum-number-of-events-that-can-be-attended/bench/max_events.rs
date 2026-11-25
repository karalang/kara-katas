// LeetCode #1353 bench -- Rust: a sweep over the days with a BinaryHeap of
// the open events' last days, smallest first through Reverse.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn max_events(events: &[[i32; 2]]) -> i32 {
    let mut by_start = events.to_vec();
    by_start.sort_by_key(|e| e[0]);
    let mut ends = BinaryHeap::new();
    let mut next = 0;
    let mut attended = 0;
    let mut day = 1;
    while next < by_start.len() || !ends.is_empty() {
        if ends.is_empty() && by_start[next][0] > day {
            day = by_start[next][0];
        }
        while next < by_start.len() && by_start[next][0] == day {
            ends.push(Reverse(by_start[next][1]));
            next += 1;
        }
        while let Some(&Reverse(end)) = ends.peek() {
            if end >= day {
                break;
            }
            ends.pop();
        }
        if ends.pop().is_some() {
            attended += 1;
        }
        day += 1;
    }
    attended
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1353;
    let mut sets: Vec<Vec<[i32; 2]>> = Vec::new();
    for _ in 0..20 {
        let mut events = Vec::new();
        for _ in 0..10000 {
            let start = 1 + next_random(&mut seed) % 10000;
            let end = start + next_random(&mut seed) % 30;
            events.push([start as i32, end as i32]);
        }
        sets.push(events);
    }
    let mut check: i64 = 0;
    for r in 0..600i64 {
        let k = (check % 20) as usize;
        let at = ((check / 20) % 10000) as usize;
        let start = 1 + (check / 7) % 10000;
        sets[k][at] = [start as i32, (start + (check / 11) % 30) as i32];
        check = (check * 31 + max_events(&sets[k]) as i64 + r) % 1000000007;
    }
    println!("600 rounds over 20 sets of 10^4 events: checksum {}", check);
}
