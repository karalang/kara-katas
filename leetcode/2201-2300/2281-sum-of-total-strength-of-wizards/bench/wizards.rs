// LeetCode #2281: Sum of Total Strength of Wizards -- the bench, the ★
// arm.

const MOD: i64 = 1000000007;

fn total_strength(strength: &[i64]) -> i64 {
    let n = strength.len();
    let mut left: Vec<i64> = vec![-1; n];
    let mut right: Vec<i64> = vec![n as i64; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..n {
        while !stack.is_empty() && strength[stack[stack.len() - 1]] >= strength[i] {
            stack.pop();
        }
        if !stack.is_empty() {
            left[i] = stack[stack.len() - 1] as i64;
        }
        stack.push(i);
    }
    stack.clear();
    for i in (0..n).rev() {
        while !stack.is_empty() && strength[stack[stack.len() - 1]] > strength[i] {
            stack.pop();
        }
        if !stack.is_empty() {
            right[i] = stack[stack.len() - 1] as i64;
        }
        stack.push(i);
    }
    let mut prefix: Vec<i64> = vec![0; n + 1];
    for i in 0..n {
        prefix[i + 1] = (prefix[i] + strength[i]) % MOD;
    }
    let mut twice: Vec<i64> = vec![0; n + 2];
    for i in 0..n + 1 {
        twice[i + 1] = (twice[i] + prefix[i]) % MOD;
    }
    let mut total = 0;
    for i in 0..n {
        let (l, r, ii) = (left[i], right[i], i as i64);
        let ends = (ii - l) * ((twice[(r + 1) as usize] - twice[i + 1] + MOD) % MOD) % MOD;
        let starts = (r - ii) * ((twice[i + 1] - twice[(l + 1) as usize] + MOD) % MOD) % MOD;
        let groups = (ends - starts + MOD) % MOD;
        total = (total + strength[i] % MOD * groups) % MOD;
    }
    total
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2281;
    let mut check = 0;
    for _ in 0..30 {
        let mut strength: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            let high = next_random(&mut seed);
            strength.push((high * 32768 + next_random(&mut seed)) % 1000000000 + 1);
        }
        check = (check * 31 + total_strength(&strength)) % 1000000007;
    }
    println!("30 armies of 10^5: checksum {check}");
}
