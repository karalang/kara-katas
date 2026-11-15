// LeetCode #2171: Removing Minimum Number of Magic Beans -- the
// benchmark's Rust mirror of beans.kara.

fn minimum_removal(beans: &[i64]) -> i64 {
    let mut sorted = beans.to_vec();
    sorted.sort();
    let n = sorted.len() as i64;
    let mut total = 0i64;
    let mut kept = 0i64;
    for i in 0..sorted.len() {
        total += sorted[i];
        kept = kept.max(sorted[i] * (n - i as i64));
    }
    total - kept
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2171i64;
    let mut row: Vec<i64> = Vec::new();
    for _ in 0..400000 {
        row.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1);
    }
    let mut check = 0i64;
    for _ in 0..100 {
        let start = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 300001) as usize;
        let removed = minimum_removal(&row[start..start + 100000]);
        check = (check * 31 + removed % 1000000007) % 1000000007;
    }
    println!("100 solves: checksum {}", check);
}
