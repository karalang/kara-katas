// LeetCode #1562: Find Latest Group of Size M -- bench: the ★ arm (group
// lengths kept at both ends, a count of groups of length m) over 20 random
// orders of 100000 positions, built once, each asked for m from 1 to 10.
// Rust mirror of latest.kara.

fn find_latest_step(arr: &[i64], m: i64) -> i64 {
    let n = arr.len();
    let mut length = vec![0i64; n + 2];
    let mut groups_of_m = 0;
    let mut latest = -1;
    for (step, &a) in arr.iter().enumerate() {
        let a = a as usize;
        let left = length[a - 1];
        let right = length[a + 1];
        let total = left + right + 1;
        if left == m {
            groups_of_m -= 1;
        }
        if right == m {
            groups_of_m -= 1;
        }
        if total == m {
            groups_of_m += 1;
        }
        length[a - left as usize] = total;
        length[a + right as usize] = total;
        if groups_of_m > 0 {
            latest = step as i64 + 1;
        }
    }
    latest
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n = 100000i64;
    let mut seed = 1562;
    let mut orders: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut arr: Vec<i64> = (1..=n).collect();
        for i in (1..n).rev() {
            let j = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (i + 1);
            arr.swap(i as usize, j as usize);
        }
        orders.push(arr);
    }
    let mut check = 0;
    let mut total = 0;
    for m in 1..=10 {
        for arr in &orders {
            let step = find_latest_step(arr, m);
            total += step;
            check = mix(check, step);
        }
    }
    println!("m from 1 to 10 over 20 orders of 100000 positions: steps sum {}, checksum {}", total, check);
}
