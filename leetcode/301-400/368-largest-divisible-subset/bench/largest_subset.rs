// Benchmark for #368 -- mirror of largest_subset.kara.

fn largest_divisible_subset(nums: &[i64]) -> Vec<i64> {
    let mut a = nums.to_vec();
    a.sort();
    let n = a.len();
    let mut size = vec![1i64; n];
    let mut next = vec![-1i64; n];
    for i in (0..n).rev() {
        for k in i + 1..n {
            if a[k] % a[i] == 0 && size[k] + 1 > size[i] {
                size[i] = size[k] + 1;
                next[i] = k as i64;
            }
        }
    }
    let mut start = 0;
    for i in 1..n {
        if size[i] > size[start] {
            start = i;
        }
    }
    let mut out = Vec::new();
    let mut at = start as i64;
    while at != -1 {
        out.push(a[at as usize]);
        at = next[at as usize];
    }
    out
}

fn main() {
    let mut seed: i64 = 368;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..200 {
        let mut taken = vec![false; 100001];
        let mut nums: Vec<i64> = Vec::new();
        while nums.len() < 1000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let high = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let v = 1 + (high * 32768 + seed / 65536) % 100000;
            if !taken[v as usize] {
                taken[v as usize] = true;
                nums.push(v);
            }
        }
        let out = largest_divisible_subset(&nums);
        total += out.len() as i64;
        for v in &out {
            checksum = (checksum * 31 + v) % 1000000007;
        }
    }
    println!("{} numbers in the answers, checksum {}", total, checksum);
}
