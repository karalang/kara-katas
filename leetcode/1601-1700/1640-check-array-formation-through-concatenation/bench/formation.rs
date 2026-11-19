// LeetCode #1640: Check Array Formation Through Concatenation -- the
// bench's Rust mirror: the ★ arm on 50000 random cases of the values 1 to
// 100 in a random order, cut into pieces of 1 to 3 and shuffled, every
// third one with two values swapped, all drawn first.

use std::collections::HashMap;

fn can_form_array(arr: &Vec<i32>, pieces: &Vec<Vec<i32>>) -> bool {
    let mut starting: HashMap<i32, usize> = HashMap::new();
    for (k, piece) in pieces.iter().enumerate() {
        starting.insert(piece[0], k);
    }
    let mut i = 0;
    while i < arr.len() {
        let Some(&k) = starting.get(&arr[i]) else {
            return false;
        };
        for &value in &pieces[k] {
            if i >= arr.len() || arr[i] != value {
                return false;
            }
            i += 1;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1640;
    let mut cases = Vec::new();
    for c in 0..50000 {
        let mut arr: Vec<i32> = (1..=100).collect();
        for k in (1..100usize).rev() {
            let j = (next_random(&mut seed) % (k as i64 + 1)) as usize;
            arr.swap(k, j);
        }
        let mut pieces: Vec<Vec<i32>> = Vec::new();
        let mut start = 0usize;
        while start < 100 {
            let end = 100.min(start + (next_random(&mut seed) % 3 + 1) as usize);
            pieces.push(arr[start..end].to_vec());
            start = end;
        }
        for k in (1..pieces.len()).rev() {
            let j = (next_random(&mut seed) % (k as i64 + 1)) as usize;
            pieces.swap(k, j);
        }
        if c % 3 == 2 {
            let a = (next_random(&mut seed) % 100) as usize;
            let b = (next_random(&mut seed) % 100) as usize;
            arr.swap(a, b);
        }
        cases.push((arr, pieces));
    }
    let mut check: i64 = 0;
    let mut trues = 0;
    for (arr, pieces) in &cases {
        let formed = can_form_array(arr, pieces);
        if formed {
            trues += 1;
        }
        check = (check * 31 + if formed { 2 } else { 1 }) % 1000000007;
    }
    println!("50000 cases of 100 values: {} can be formed, checksum {}", trues, check);
}
