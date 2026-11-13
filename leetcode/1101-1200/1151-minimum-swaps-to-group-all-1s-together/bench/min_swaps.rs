// LeetCode #1151: Minimum Swaps to Group All 1's Together -- the Rust
// mirror of the ★ arm: a window as long as the count of ones slides along
// the list, and the answer is the count less the most ones it holds.

fn min_swaps(data: &[i64]) -> i64 {
    let k: i64 = data.iter().sum();
    if k == 0 {
        return 0;
    }
    let k = k as usize;
    let mut inside: i64 = 0;
    for i in 0..k {
        inside += data[i];
    }
    let mut most = inside;
    for i in k..data.len() {
        inside += data[i] - data[i - k];
        most = most.max(inside);
    }
    k as i64 - most
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1151;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for l in 0..16 {
        let ones = 1 + l % 7;
        lists.push((0..100000).map(|_| if next_random(&mut seed) % 8 < ones { 1 } else { 0 }).collect());
    }
    let (mut total, mut check) = (0i64, 0i64);
    for r in 0..3000 {
        let l = r % 16;
        for _ in 0..64 {
            let at = (next_random(&mut seed) * 3) as usize;
            lists[l][at] = 1 - lists[l][at];
        }
        let s = min_swaps(&lists[l]);
        total += s;
        check = (check * 31 + s) % 1000000007;
    }
    println!("3000 rounds over 16 lists of 100000 bits: swaps total {total}, checksum {check}");
}
