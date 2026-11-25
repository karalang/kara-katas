// LeetCode #1394 bench, Rust mirror of the ★ arm.

fn find_lucky(arr: &[i32]) -> i32 {
    let mut count: Vec<i32> = vec![0; 501];
    for &x in arr {
        count[x as usize] += 1;
    }
    for x in (1..=500).rev() {
        if count[x as usize] == x {
            return x;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 500;
    let mut seed: i64 = 1394;
    let mut arr: Vec<i32> = Vec::new();
    for _ in 0..n {
        arr.push((1 + next_random(&mut seed) % 40) as i32);
    }
    let mut check: i64 = 0;
    for _ in 0..600000 {
        seed = (seed + check) % 2147483648;
        let i = next_random(&mut seed) % n;
        arr[i as usize] = (1 + next_random(&mut seed) % 40) as i32;
        check = (check * 131 + find_lucky(&arr) as i64 + 1) % 1000000007;
    }
    println!("600000 rounds over 500 values: checksum {}", check);
}
