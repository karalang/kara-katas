// Benchmark: LeetCode #1089 Duplicate Zeros -- mirrors duplicate_zeros.kara:
// count the zeros, then walk back from the end writing each digit at its
// place shifted by the zeros up to it, over 200 random arrays of 10^4
// digits built once, each copied and duplicated in each of 100 rounds.

fn duplicate_zeros(arr: &mut Vec<i64>) {
    let n = arr.len() as i64;
    let mut zeros: i64 = 0;
    for &x in arr.iter() {
        if x == 0 {
            zeros += 1;
        }
    }
    for i in (0..n).rev() {
        if i + zeros < n {
            arr[(i + zeros) as usize] = arr[i as usize];
        }
        if arr[i as usize] == 0 {
            zeros -= 1;
            if i + zeros < n {
                arr[(i + zeros) as usize] = 0;
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1089;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..200 {
        let mut arr: Vec<i64> = Vec::new();
        for _ in 0..10000 {
            let r = next_random(&mut seed) % 15;
            arr.push(if r < 5 { 0 } else { r - 5 });
        }
        arrays.push(arr);
    }
    let mut zeros: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..100i64 {
        for (k, a) in arrays.iter().enumerate() {
            let mut work = a.clone();
            duplicate_zeros(&mut work);
            let at = ((round * 7919 + k as i64 * 31) % 10000) as usize;
            if work[at] == 0 {
                zeros += 1;
            }
            check = (check * 31 + work[at] * 10 + work[9999]) % 1000000007;
        }
    }
    println!("100 rounds over 200 arrays of 10^4 digits: {} zeros sampled, checksum {}", zeros, check);
}
