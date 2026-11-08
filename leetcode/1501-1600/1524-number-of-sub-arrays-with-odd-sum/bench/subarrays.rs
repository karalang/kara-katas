// LeetCode #1524: Number of Sub-arrays With Odd Sum -- bench: the ★ arm
// over 100 random arrays of 1 to 100000 numbers from 1 to 100, built once
// and answered 20 times.

fn num_of_subarrays(arr: &[i64]) -> i64 {
    let modulus = 1000000007;
    let mut odd = 0;
    let mut even = 1;
    let mut sum = 0;
    let mut answer = 0;
    for &x in arr {
        sum += x;
        if sum % 2 == 1 {
            answer = (answer + even) % modulus;
            odd += 1;
        } else {
            answer = (answer + odd) % modulus;
            even += 1;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1524i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let mut arr: Vec<i64> = Vec::new();
        for _ in 0..n {
            arr.push(next_random(&mut seed) % 100 + 1);
        }
        arrays.push(arr);
    }
    let mut check = 0;
    for _ in 0..20 {
        for arr in &arrays {
            check = mix(check, num_of_subarrays(arr));
        }
    }
    println!("20 passes over 100 arrays of up to 100000 numbers: checksum {}", check);
}
