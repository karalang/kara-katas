// LeetCode #1176: Diet Plan Performance -- the ★ arm's bench in Rust: one
// window of k days slid across the plan, its sum kept as it goes, each
// window scored as it is reached. The same plan and the same 2000 calls.

fn diet_plan_performance(calories: &[i64], k: usize, lower: i64, upper: i64) -> i64 {
    let mut points = 0;
    let mut total = 0;
    for (i, &c) in calories.iter().enumerate() {
        total += c;
        if i >= k {
            total -= calories[i - k];
        }
        if i + 1 >= k {
            if total < lower {
                points -= 1;
            } else if total > upper {
                points += 1;
            }
        }
    }
    points
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1176;
    let calories: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 20001).collect();
    let calls = 2000;
    let mut check: i64 = 0;
    for _ in 0..calls {
        let k = 1 + next_random(&mut seed) % 100000;
        let mean = 10000 * k;
        let spread = next_random(&mut seed) % 100 * k;
        let p = diet_plan_performance(&calories, k as usize, mean - spread, mean + spread);
        check = (check * 131 + p + 100000) % 1000000007;
    }
    println!("{} calls: checksum {}", calls, check);
}
