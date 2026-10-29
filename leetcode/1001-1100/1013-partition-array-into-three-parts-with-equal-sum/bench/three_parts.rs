// LeetCode #1013: Partition Array Into Three Parts With Equal Sum -- bench
// Mirrors three_parts.kara; see ../README.md § Benchmarks.

fn can_three_parts_equal_sum(arr: &[i64]) -> bool {
    let mut total = 0;
    for &x in arr.iter() {
        total += x;
    }
    if total % 3 != 0 {
        return false;
    }
    let target = total / 3;
    let mut prefix = 0;
    let mut cuts = 0;
    for i in 0..arr.len() - 1 {
        prefix += arr[i];
        if cuts == 0 && prefix == target {
            cuts = 1;
        } else if cuts == 1 && prefix == 2 * target {
            return true;
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: usize = 50000;
    let rounds = 10000;
    let mut seed = 1013;
    let mut arr: Vec<i64> = Vec::new();
    let mut total = 0;
    for _ in 0..count {
        let x = next_random(&mut seed) % 7 - 2;
        arr.push(x);
        total += x;
    }
    arr[count - 1] -= total % 3;
    let mut yes = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        let at = ((hi * 32768 + lo) % count as i64) as usize;
        arr[at] += 3 * (next_random(&mut seed) % 3 - 1);
        let answer = can_three_parts_equal_sum(&arr);
        if answer {
            yes += 1;
        }
        check = (check * 2 + if answer { 1 } else { 0 }) % 1000000007;
    }
    println!("{} rounds over {} values: {} split, checksum {}", rounds, count, yes, check);
}
