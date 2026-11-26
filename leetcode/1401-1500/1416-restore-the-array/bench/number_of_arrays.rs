// LeetCode #1416 bench, Rust: ways[i] counts the arrays the digits from i
// on can be read as, workload and checksum as number_of_arrays.kara.

fn number_of_arrays(s: &str, k: i32) -> i32 {
    let modulus: i64 = 1000000007;
    let digits = s.as_bytes();
    let n = digits.len();
    let mut ways: Vec<i64> = vec![0; n + 1];
    ways[n] = 1;
    for i in (0..n).rev() {
        if digits[i] == b'0' {
            continue;
        }
        let mut number: i64 = 0;
        let mut j = i;
        while j < n {
            number = number * 10 + (digits[j] - b'0') as i64;
            if number > k as i64 {
                break;
            }
            ways[i] = (ways[i] + ways[j + 1]) % modulus;
            j += 1;
        }
    }
    ways[0] as i32
}

fn main() {
    let mut seed: i64 = 1416;
    let mut pool = String::new();
    let mut last_zero = true;
    for _ in 0..200000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let r = seed / 65536;
        let zero = !last_zero && r % 10 == 0;
        let d = if zero { 0 } else { 1 + r % 9 };
        pool.push_str(&format!("{}", d));
        last_zero = zero;
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let mut start = (seed / 65536 % 100000) as usize;
        while &pool[start..start + 1] == "0" {
            start += 1;
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let k = 1 + seed % 1000000000;
        check = (check * 131 + number_of_arrays(&pool[start..start + 100000], k as i32) as i64) % 1000000007;
    }
    println!("100 windows of 10^5 digits: checksum {}", check);
}
