// LeetCode #1824: Minimum Sideway Jumps -- the bench in Rust: the ★ arm
// over 50 calls on roads of 250000 to 499999 steps cut from one road of
// 5 * 10^5 steps with an obstacle at half its points, built once, each
// road's length drawn from the checksum so far and its last point cleared.

fn min_side_jumps(obstacles: Vec<i64>) -> i64 {
    let never = obstacles.len() as i64 + 1;
    let mut jumps = [1i64, 0, 1];
    for i in 1..obstacles.len() {
        if obstacles[i] > 0 {
            jumps[(obstacles[i] - 1) as usize] = never;
        }
        let best = *jumps.iter().min().unwrap() + 1;
        for lane in 0..3 {
            if obstacles[i] != lane as i64 + 1 {
                jumps[lane] = jumps[lane].min(best);
            }
        }
    }
    *jumps.iter().min().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1824;
    let mut base: Vec<i64> = vec![0; 500001];
    for i in 1..500000 {
        if next_random(&mut seed) % 2 == 0 {
            base[i] = 1 + next_random(&mut seed) % 3;
        }
    }
    let mut check: i64 = 0;
    for call in 0..50 {
        let n = (250000 + (check + call) % 250000) as usize;
        let mut road = base[..n + 1].to_vec();
        road[n] = 0;
        check = (check * 31 + min_side_jumps(road)) % 1000000007;
    }
    println!("50 calls: checksum {}", check);
}
