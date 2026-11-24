// LeetCode #1345 bench in Rust: the ★ arm (a breadth-first search over
// i - 1, i + 1 and the indices of the same value, gathered in a `HashMap`
// and each value's list taken out the first time it is used) on the same
// 10 arrays of 5 * 10^4 values and 30 passes.
use std::collections::{HashMap, VecDeque};

fn min_jumps(arr: &[i32]) -> i32 {
    let n = arr.len() as i64;
    let mut places: HashMap<i32, Vec<i64>> = HashMap::new();
    for i in 0..n {
        places.entry(arr[i as usize]).or_default().push(i);
    }
    let mut steps = vec![-1i32; n as usize];
    steps[0] = 0;
    let mut queue: VecDeque<i64> = VecDeque::new();
    queue.push_back(0);
    while let Some(i) = queue.pop_front() {
        if i == n - 1 {
            return steps[i as usize];
        }
        let mut next = places.remove(&arr[i as usize]).unwrap_or_default();
        next.push(i - 1);
        next.push(i + 1);
        for &j in &next {
            if j >= 0 && j < n && steps[j as usize] < 0 {
                steps[j as usize] = steps[i as usize] + 1;
                queue.push_back(j);
            }
        }
    }
    steps[(n - 1) as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 50000usize;
    let mut seed = 1345;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for a in 0..10 {
        let mut arr = Vec::with_capacity(n);
        for i in 0..n {
            if a % 2 == 0 {
                arr.push((1 + next_random(&mut seed) % 1000) as i32);
            } else {
                arr.push((i / 2) as i32);
            }
        }
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for pass in 0..30 {
        for a in 0..10 {
            arrays[a][(check % n as i64) as usize] = ((check / 7) % 25000) as i32;
            let answer = min_jumps(&arrays[a]);
            check = (check * 31 + answer as i64 + pass) % 1000000007;
        }
    }
    println!("30 passes over 10 arrays of 5 * 10^4: checksum {}", check);
}
