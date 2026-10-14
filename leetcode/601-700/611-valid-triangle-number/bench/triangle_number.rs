// Benchmark mirror for #611: the same workload and algorithm as
// triangle_number.kara (sort, then two pointers).

fn triangle_number(nums: &[i64]) -> i64 {
    let mut a = nums.to_vec();
    a.sort();
    let mut count = 0i64;
    for k in 2..a.len() {
        let mut i = 0usize;
        let mut j = k - 1;
        while i < j {
            if a[i] + a[j] > a[k] {
                count += (j - i) as i64;
                j -= 1;
            } else {
                i += 1;
            }
        }
    }
    count
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays = 20i64;
    let rounds = 600i64;
    let mut seed: i64 = 611;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..arrays {
        let bound = 100 + step(&mut seed) % 901;
        let nums: Vec<i64> = (0..1000).map(|_| step(&mut seed) % (bound + 1)).collect();
        all.push(nums);
    }
    let (mut total, mut checksum) = (0i64, 0i64);
    for r in 0..rounds {
        let got = triangle_number(&all[((r * 7) % arrays) as usize]);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    println!("{} arrays, {} rounds: {} triangles, checksum {}", arrays, rounds, total, checksum);
}
