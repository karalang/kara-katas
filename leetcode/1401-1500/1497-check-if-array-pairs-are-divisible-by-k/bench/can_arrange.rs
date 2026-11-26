// LeetCode #1497: Check If Array Pairs Are Divisible by k -- the bench in
// Rust, mirroring can_arrange.kara: each value's remainder by k counted.

fn can_arrange(arr: &[i32], k: i32) -> bool {
    let mut count = vec![0i64; k as usize];
    for &x in arr {
        count[((x % k + k) % k) as usize] += 1;
    }
    if count[0] % 2 != 0 {
        return false;
    }
    for r in 1..k as usize {
        if count[r] != count[k as usize - r] {
            return false;
        }
    }
    true
}

fn main() {
    let mut seed: i64 = 1497;
    let mut arr: Vec<i32> = Vec::new();
    for _ in 0..50000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let x = seed / 65536 * 30011 % 2000000001 - 1000000000;
        arr.push(x as i32);
        arr.push((1000 * (seed % 7) - x) as i32);
    }
    let mut check: i64 = 0;
    for call in 0..1000i64 {
        let k = if call % 2 == 0 { 1000 } else { 1 + (check + call) % 100000 };
        let at = ((check * 7 + call) % 100000) as usize;
        arr[at] = (arr[at] as i64 + if call % 4 < 2 { 1000 } else { -1000 }) as i32;
        let yes = can_arrange(&arr, k as i32);
        check = (check * 31 + k + if yes { 2 } else { 1 }) % 1000000007;
    }
    println!("1000 calls over 100000 values: checksum {}", check);
}
