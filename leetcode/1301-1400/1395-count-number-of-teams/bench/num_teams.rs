// LeetCode #1395 bench, Rust mirror of the ★ arm.

fn num_teams(rating: &[i32]) -> i32 {
    let n = rating.len();
    let mut teams = 0;
    for j in 0..n {
        let (mut less_left, mut greater_left) = (0, 0);
        let (mut less_right, mut greater_right) = (0, 0);
        for i in 0..j {
            if rating[i] < rating[j] {
                less_left += 1;
            } else {
                greater_left += 1;
            }
        }
        for k in j + 1..n {
            if rating[k] < rating[j] {
                less_right += 1;
            } else {
                greater_right += 1;
            }
        }
        teams += less_left * greater_right + greater_left * less_right;
    }
    teams
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 1000;
    let mut seed: i64 = 1395;
    let mut rating: Vec<i32> = (1..=n).map(|v| (v * 97) as i32).collect();
    for i in (1..n).rev() {
        let j = next_random(&mut seed) % (i + 1);
        rating.swap(i as usize, j as usize);
    }
    let mut check: i64 = 0;
    for _ in 0..300 {
        seed = (seed + check) % 2147483648;
        let a = next_random(&mut seed) % n;
        let b = next_random(&mut seed) % n;
        rating.swap(a as usize, b as usize);
        check = (check * 131 + num_teams(&rating) as i64) % 1000000007;
    }
    println!("300 rounds over 1000 soldiers: checksum {}", check);
}
