// LeetCode #1588: Sum of All Odd Length Subarrays -- the bench in Rust,
// mirroring odd_subarrays.kara.

fn sum_odd_length_subarrays(arr: &[i32]) -> i32 {
    let n = arr.len() as i64;
    let mut total: i32 = 0;
    for (i, &v) in arr.iter().enumerate() {
        let i = i as i64;
        let through = (i + 1) * (n - i);
        total += ((through + 1) / 2) as i32 * v;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1588;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..200000 {
        let n = next_random(&mut seed) % 100 + 1;
        let arr: Vec<i32> = (0..n).map(|_| (next_random(&mut seed) % 1000 + 1) as i32).collect();
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for arr in &arrays {
        let answer = sum_odd_length_subarrays(arr) as i64;
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    println!("200000 arrays of 1 to 100 values: total {}, checksum {}", total, check);
}
