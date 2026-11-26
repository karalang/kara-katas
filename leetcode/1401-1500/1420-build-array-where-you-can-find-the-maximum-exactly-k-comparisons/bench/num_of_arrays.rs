fn num_of_arrays(n: i32, m: i32, k: i32) -> i32 {
    let modulus: i64 = 1000000007;
    let m = m as usize;
    let k = k as usize;
    let mut ways: Vec<Vec<i64>> = vec![vec![0; k + 1]; m + 1];
    if k >= 1 {
        for j in 1..=m {
            ways[j][1] = 1;
        }
    }
    for _ in 1..n {
        let mut next: Vec<Vec<i64>> = vec![vec![0; k + 1]; m + 1];
        for c in 1..=k {
            let mut below: i64 = 0;
            for j in 1..=m {
                next[j][c] = (ways[j][c] * j as i64 + below) % modulus;
                below = (below + ways[j][c - 1]) % modulus;
            }
        }
        ways = next;
    }
    let mut total: i64 = 0;
    for j in 1..=m {
        total = (total + ways[j][k]) % modulus;
    }
    total as i32
}

fn main() {
    let mut seed: i64 = 1420;
    let mut check: i64 = 0;
    for _ in 0..1000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let k = seed / 65536 % 51;
        check = (check * 131 + num_of_arrays(50, 100, k as i32) as i64) % 1000000007;
    }
    println!("1000 values of k at n = 50, m = 100: checksum {}", check);
}
