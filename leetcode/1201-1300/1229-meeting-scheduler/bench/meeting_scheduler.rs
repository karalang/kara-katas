// LeetCode #1229 bench: the ★ arm in Rust, over the same 50 pairs of
// schedules and 10 durations as the Kāra bench.

fn min_available_duration(slots1: &[Vec<i64>], slots2: &[Vec<i64>], duration: i64) -> Vec<i64> {
    let mut a = slots1.to_vec();
    let mut b = slots2.to_vec();
    a.sort();
    b.sort();
    let (mut i, mut j) = (0, 0);
    while i < a.len() && j < b.len() {
        let start = a[i][0].max(b[j][0]);
        let end = a[i][1].min(b[j][1]);
        if end - start >= duration {
            return vec![start, start + duration];
        }
        if a[i][1] < b[j][1] {
            i += 1;
        } else {
            j += 1;
        }
    }
    vec![]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn slots(seed: &mut i64, count: i64, width: i64, gap: i64) -> Vec<Vec<i64>> {
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut at = next_random(seed) % (gap + 1);
    for _ in 0..count {
        let end = at + next_random(seed) % width + 1;
        out.push(vec![at, end]);
        at = end + next_random(seed) % gap + 1;
    }
    for i in (1..out.len()).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        out.swap(i, j);
    }
    out
}

fn main() {
    let mut seed = 1229;
    let mut pairs = Vec::new();
    for _ in 0..50 {
        let a = slots(&mut seed, 10000, 50000, 50000);
        let b = slots(&mut seed, 10000, 50000, 50000);
        pairs.push((a, b));
    }
    let mut check: i64 = 0;
    for (a, b) in &pairs {
        for k in 1..=10 {
            let answer = min_available_duration(a, b, k * 4000);
            let v = if answer.is_empty() { 7 } else { answer[0] };
            check = (check * 131 + v) % 1000000007;
        }
    }
    println!("50 pairs of 10^4 slots, 10 durations: checksum {check}");
}
