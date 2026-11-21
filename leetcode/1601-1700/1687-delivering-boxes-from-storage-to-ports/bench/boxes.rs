// LeetCode #1687: Delivering Boxes from Storage to Ports -- the bench's Rust
// mirror: the ★ arm on 50 random problems of 100000 boxes, all drawn first,
// each answered 20 times.

use std::collections::VecDeque;

fn deliver(boxes: &[Vec<i32>], _ports_count: i32, max_boxes: i32, max_weight: i32) -> i32 {
    let n = boxes.len();
    let mut changes = vec![0i32; n];
    let mut weight = vec![0i64; n + 1];
    for k in 0..n {
        weight[k + 1] = weight[k] + boxes[k][1] as i64;
        if k > 0 {
            changes[k] = changes[k - 1] + if boxes[k][0] != boxes[k - 1][0] { 1 } else { 0 };
        }
    }
    let mut trips = vec![0i32; n + 1];
    let mut starts: VecDeque<usize> = VecDeque::new();
    for i in 1..=n {
        let j = i - 1;
        let cost = trips[j] - changes[j];
        while let Some(&back) = starts.back() {
            if trips[back] - changes[back] >= cost {
                starts.pop_back();
            } else {
                break;
            }
        }
        starts.push_back(j);
        while let Some(&front) = starts.front() {
            if (i - front) as i64 > max_boxes as i64 || weight[i] - weight[front] > max_weight as i64 {
                starts.pop_front();
            } else {
                break;
            }
        }
        let front = *starts.front().unwrap();
        trips[i] = trips[front] - changes[front] + changes[i - 1] + 2;
    }
    trips[n]
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let size = 100000;
    let rounds = 20;
    let mut seed = 1687;
    let mut problems: Vec<(Vec<Vec<i32>>, i32, i32, i32)> = Vec::new();
    for _ in 0..count {
        let ports_count = next_random(&mut seed) % 100 + 1;
        let max_boxes = next_random(&mut seed) % 1000 + 1;
        let max_weight = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 99001 + 1000;
        let mut boxes = Vec::new();
        for _ in 0..size {
            let port = next_random(&mut seed) % ports_count + 1;
            let weight = next_random(&mut seed) % 1000 + 1;
            boxes.push(vec![port as i32, weight as i32]);
        }
        problems.push((boxes, ports_count as i32, max_boxes as i32, max_weight as i32));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (boxes, ports_count, max_boxes, max_weight) in problems.iter() {
            let answer = deliver(boxes, *ports_count, *max_boxes, *max_weight) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} problems of {size} boxes, {rounds} rounds: {total} trips, checksum {check}");
}
