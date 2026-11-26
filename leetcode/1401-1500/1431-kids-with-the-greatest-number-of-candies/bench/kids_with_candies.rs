fn kids_with_candies(candies: &[i32], extra_candies: i32) -> Vec<bool> {
    let most = *candies.iter().max().unwrap();
    candies.iter().map(|&c| c + extra_candies >= most).collect()
}

fn main() {
    let mut seed: i64 = 1431;
    let mut pool: Vec<i32> = Vec::with_capacity(1000000);
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push((1 + seed / 65536 % 100) as i32);
    }
    let mut check: i64 = 0;
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let start = (seed / 65536 % 999901) as usize;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let extra = (1 + seed / 65536 % 50) as i32;
        let mut bits: i64 = 0;
        for (j, &b) in kids_with_candies(&pool[start..start + 100], extra).iter().enumerate() {
            if b {
                bits += j as i64 + 1;
            }
        }
        check = (check * 131 + bits) % 1000000007;
    }
    println!("10^6 windows of 100 kids: checksum {}", check);
}
