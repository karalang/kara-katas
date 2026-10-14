// Benchmark for #565: Rust mirror of the ★ arm (walk each cycle once);
// see array_nesting.kara.

fn array_nesting(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut visited = vec![false; n];
    let mut best = 0;
    for start in 0..n {
        if visited[start] {
            continue;
        }
        let mut length = 0;
        let mut i = start;
        while !visited[i] {
            visited[i] = true;
            i = nums[i] as usize;
            length += 1;
        }
        best = best.max(length);
    }
    best
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 20;
    let rounds: i64 = 100;
    let n: i64 = 100000;
    let mut seed: i64 = 565;
    let mut perms: Vec<Vec<i64>> = Vec::new();
    for g in 0..count {
        let mut nums: Vec<i64> = (0..n).collect();
        if g % 2 == 0 {
            let mut i = n - 1;
            while i > 0 {
                let hi = step(&mut seed);
                let j = (hi * 32768 + step(&mut seed)) % (i + 1);
                nums.swap(i as usize, j as usize);
                i -= 1;
            }
        } else {
            let mut start = 0;
            while start < n {
                let length = (1 + step(&mut seed) % 2000).min(n - start);
                for j in 0..length {
                    nums[(start + j) as usize] = start + (j + 1) % length;
                }
                start += length;
            }
        }
        perms.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let got = array_nesting(&perms[((round * 7 + g) % count) as usize]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} permutations of {}, {} rounds: total {}, checksum {}", count, n, rounds, total, checksum);
}
