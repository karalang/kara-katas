// LeetCode #1652: Defuse the Bomb -- the bench's Rust mirror: the ★ arm on
// 400 random codes of 100000 numbers from 1 to 100, each with a k from
// -99999 to 99999, all drawn first.

fn decrypt(code: &[i32], k: i32) -> Vec<i32> {
    let n = code.len() as i64;
    let mut answer = vec![0i32; n as usize];
    if k == 0 {
        return answer;
    }
    let k = k as i64;
    let (mut start, mut end) = if k > 0 { (1, k) } else { (n + k, n - 1) };
    let mut sum: i32 = 0;
    for j in start..=end {
        sum += code[(j % n) as usize];
    }
    for i in 0..n as usize {
        answer[i] = sum;
        sum -= code[(start % n) as usize];
        start += 1;
        end += 1;
        sum += code[(end % n) as usize];
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1652;
    let n: i64 = 100000;
    let mut codes: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..400 {
        let code: Vec<i32> = (0..n).map(|_| (next_random(&mut seed) % 100 + 1) as i32).collect();
        let k = (next_random(&mut seed) % (2 * n - 1) - (n - 1)) as i32;
        codes.push((code, k));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (code, k) in &codes {
        for &x in decrypt(code, *k).iter() {
            let x = x as i64;
            total += x;
            check = (check * 31 + x + 1) % 1000000007;
        }
    }
    println!("400 codes of 100000 numbers: answers sum to {}, checksum {}", total, check);
}
