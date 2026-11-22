// LeetCode #2742: Painting the Walls -- the bench (walls.kara in Rust):
// a knapsack over the walls covered.

fn paint_walls(cost: &[i64], time: &[i64]) -> i64 {
    let n = cost.len();
    let far = i64::MAX / 2;
    let mut least: Vec<i64> = vec![far; n + 1];
    least[0] = 0;
    for i in 0..n {
        for j in (1..=n).rev() {
            let from = (j as i64 - time[i] - 1).max(0) as usize;
            least[j] = least[j].min(least[from] + cost[i]);
        }
    }
    least[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let n = 500;
    let rounds: i64 = 100;
    let mut seed = 2742;
    let mut cases: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..count {
        let mut cost: Vec<i64> = Vec::new();
        for _ in 0..n {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            cost.push((hi * 32768 + lo) % 1000000 + 1);
        }
        let mut time: Vec<i64> = Vec::new();
        for _ in 0..n {
            time.push(next_random(&mut seed) % 20 + 1);
        }
        cases.push((cost, time));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (cost, time) in cases.iter() {
            let least = paint_walls(cost, time);
            sum += least;
            check = (check * 31 + least + r) % 1000000007;
        }
    }
    println!("{} cases of {} walls, {} rounds: costs sum to {}, checksum {}", count, n, rounds, sum, check);
}
