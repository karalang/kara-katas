// LeetCode #2305: Fair Distribution of Cookies -- the bench, the ★ arm in
// Rust. Backtrack each bag over the children whose load stays under the
// best so far, trying only the first child with nothing yet.

fn place(cookies: &[i64], i: usize, loads: &mut Vec<i64>, best: &mut i64) {
    if i == cookies.len() {
        *best = (*best).min(*loads.iter().max().unwrap());
        return;
    }
    for c in 0..loads.len() {
        if loads[c] + cookies[i] < *best {
            loads[c] += cookies[i];
            place(cookies, i + 1, loads, best);
            loads[c] -= cookies[i];
        }
        if loads[c] == 0 {
            break;
        }
    }
}

fn distribute_cookies(cookies: &[i64], k: usize) -> i64 {
    let mut loads = vec![0i64; k];
    let mut best = i64::MAX;
    place(cookies, 0, &mut loads, &mut best);
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2305;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let mut cookies = Vec::new();
        for _ in 0..8 {
            let hi = next_random(&mut seed);
            cookies.push((hi * 32768 + next_random(&mut seed)) % 100000 + 1);
        }
        lists.push(cookies);
    }
    let mut check: i64 = 0;
    for p in 0..50 {
        for a in 0..2000 {
            check = (check * 31 + distribute_cookies(&lists[a], 2 + (a + p) % 7)) % 1000000007;
        }
    }
    println!("50 passes over 2000 lists of 8 bags: checksum {}", check);
}
