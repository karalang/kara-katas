// LeetCode #2283: Check if Number Has Equal Digit Count and Digit Value
// -- the bench, the ★ arm.

fn digit_count(num: &str) -> bool {
    let mut counts = [0i64; 10];
    for c in num.chars() {
        counts[c.to_digit(10).unwrap() as usize] += 1;
    }
    for (i, c) in num.chars().enumerate() {
        if counts[i] != c.to_digit(10).unwrap() as i64 {
            return false;
        }
    }
    true
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let known = ["1210", "2020", "21200", "3211000", "42101000", "521001000", "6210001000"];
    let mut seed = 2283;
    let mut nums: Vec<String> = Vec::new();
    for k in 0..100000 {
        if k % 8 == 0 {
            nums.push(known[(next_random(&mut seed) % 7) as usize].to_string());
        } else {
            let n = next_random(&mut seed) % 10 + 1;
            let mut num = String::new();
            for _ in 0..n {
                num.push((b'0' + (next_random(&mut seed) % (n.min(9) + 1)) as u8) as char);
            }
            nums.push(num);
        }
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        let mut held = 0;
        for num in &nums {
            if digit_count(num) {
                held += 1;
            }
        }
        check = (check * 31 + held) % 1000000007;
    }
    println!("100 passes over 10^5 strings: checksum {check}");
}
