// LeetCode #1449 Form Largest Integer With Digits That Add up to Target: the
// bench, a mirror of largest_number.kara.

fn largest_number(cost: &[i32], target: i32) -> String {
    // the most digits each cost from 0 to target buys exactly, -1 when it
    // buys none; then the digits taken from 9 down, each while what is left
    // still buys one digit fewer
    let target = target as usize;
    let mut most: Vec<i64> = vec![-1; target + 1];
    most[0] = 0;
    for t in 1..=target {
        for &c in cost.iter() {
            let c = c as usize;
            if c <= t && most[t - c] >= 0 {
                most[t] = most[t].max(most[t - c] + 1);
            }
        }
    }
    if most[target] < 0 {
        return "0".to_string();
    }
    let mut digits = String::new();
    let mut left = target;
    for d in (0..9).rev() {
        let c = cost[d] as usize;
        while c <= left && most[left - c] == most[left] - 1 {
            digits.push((b'1' + d as u8) as char);
            left -= c;
        }
    }
    digits
}

fn main() {
    // 5000 cases with the constraints' most target, 5000, each with nine
    // costs drawn from 1 to 50, each answer's digits folded to a checksum
    let mut seed: i64 = 1449;
    let mut check: i64 = 0;
    for _ in 0..5000 {
        let mut cost: Vec<i32> = Vec::new();
        for _ in 0..9 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            cost.push((1 + seed / 65536 % 50) as i32);
        }
        for b in largest_number(&cost, 5000).bytes() {
            check = (check * 131 + b as i64) % 1000000007;
        }
    }
    println!("5000 targets of 5000: checksum {}", check);
}
