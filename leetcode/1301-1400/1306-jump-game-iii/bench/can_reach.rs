// LeetCode #1306 bench in Rust: the ★ arm (a breadth-first walk from the
// start in a `VecDeque`, each place queued once) on the same 10 arrays and
// 300 passes.
use std::collections::VecDeque;

fn can_reach(arr: &[i64], start: i64) -> bool {
    let n = arr.len() as i64;
    let mut seen = vec![false; arr.len()];
    let mut queue = VecDeque::new();
    queue.push_back(start);
    seen[start as usize] = true;
    while let Some(i) = queue.pop_front() {
        let v = arr[i as usize];
        if v == 0 {
            return true;
        }
        for j in [i + v, i - v] {
            if j >= 0 && j < n && !seen[j as usize] {
                seen[j as usize] = true;
                queue.push_back(j);
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 50000i64;
    let mut seed = 1306i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut arr: Vec<i64> = (0..n).map(|_| 1 + next_random(&mut seed) % 10).collect();
        let at = next_random(&mut seed) % n;
        arr[at as usize] = 0;
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for pass in 0..300i64 {
        for arr in arrays.iter_mut() {
            arr[(check % n) as usize] = (check / 7) % 11;
            let start = (check / 13) % n;
            let got = can_reach(arr, start);
            check = (check * 31 + if got { 1 } else { 2 } + pass) % 1000000007;
        }
    }
    println!("300 passes over 10 arrays of 5 * 10^4: checksum {check}");
}
