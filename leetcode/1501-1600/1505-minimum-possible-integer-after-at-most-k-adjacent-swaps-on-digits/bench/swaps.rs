// LeetCode #1505: Minimum Possible Integer After at Most K Adjacent Swaps On
// Digits -- the benchmark, the same algorithm as swaps.kara: per-digit
// queues of indices and a Fenwick tree of the digits already taken.

fn taken_before(tree: &[i64], i: usize) -> i64 {
    let (mut s, mut at) = (0, i);
    while at > 0 {
        s += tree[at];
        at -= at & at.wrapping_neg();
    }
    s
}

fn take(tree: &mut [i64], i: usize) {
    let mut at = i + 1;
    while at < tree.len() {
        tree[at] += 1;
        at += at & at.wrapping_neg();
    }
}

fn min_integer(num: &str, k: i64) -> String {
    let digits = num.as_bytes();
    let n = digits.len();
    let mut wh: Vec<Vec<usize>> = vec![Vec::new(); 10];
    for i in 0..n {
        wh[(digits[i] - b'0') as usize].push(i);
    }
    let mut head = [0usize; 10];
    let mut tree = vec![0i64; n + 1];
    let mut left = k;
    let mut out = String::new();
    for _ in 0..n {
        for d in 0..10 {
            if head[d] < wh[d].len() {
                let i = wh[d][head[d]];
                let cost = i as i64 - taken_before(&tree, i);
                if cost <= left {
                    left -= cost;
                    head[d] += 1;
                    take(&mut tree, i);
                    out.push((b'0' + d as u8) as char);
                    break;
                }
            }
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1505;
    let mut cases: Vec<(String, i64)> = Vec::new();
    for c in 0..60i64 {
        let digits = c % 10 + 1;
        let num: String = (0..30000).map(|_| (48 + next_random(&mut seed) % digits) as u8 as char).collect();
        let k = next_random(&mut seed) * (c % 7 + 1) * 50;
        cases.push((num, k));
    }
    let mut check = 0;
    for (num, k) in &cases {
        for b in min_integer(num, *k).bytes() {
            check = mix(check, b as i64 - 48);
        }
    }
    println!("60 numbers of 30000 digits: checksum {check}");
}
