// LeetCode #1230 bench: the ★ arm in Rust, over the same 200 sets of 1000
// coins as the Kāra bench.

fn probability_of_heads(prob: &[f64], target: usize) -> f64 {
    let mut ways = vec![0.0; target + 1];
    ways[0] = 1.0;
    for &p in prob {
        for j in (1..=target).rev() {
            ways[j] = ways[j] * (1.0 - p) + ways[j - 1] * p;
        }
        ways[0] *= 1.0 - p;
    }
    ways[target]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1230;
    let mut sets: Vec<Vec<f64>> = Vec::new();
    let mut targets: Vec<usize> = Vec::new();
    for _ in 0..200 {
        sets.push((0..1000).map(|_| (next_random(&mut seed) % 1001) as f64 / 1000.0).collect());
        targets.push((next_random(&mut seed) % 1001) as usize);
    }
    let mut total = 0.0;
    for s in 0..200 {
        total += probability_of_heads(&sets[s], targets[s]);
    }
    println!("200 sets of 1000 coins: total {:.6}", total);
}
