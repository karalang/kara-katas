// Benchmark for #561: Rust mirror of the ★ arm (sort, then every other
// number); see array_partition.kara. `sort` is std's stable sort, as
// Kāra's `Vec.sort` is.

fn array_pair_sum(mut nums: Vec<i64>) -> i64 {
    nums.sort();
    let mut sum = 0;
    for i in (0..nums.len()).step_by(2) {
        sum += nums[i];
    }
    sum
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let n = 20000;
    let rounds = 50;
    let mut seed: i64 = 561;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            nums.push(step(&mut seed) % 20001 - 10000);
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let s = array_pair_sum(arrays[(round * 7 + g) % count].clone());
            total += s;
            checksum = (checksum * 31 + s + 1000000000) % 1000000007;
        }
    }
    println!("{} arrays of {}, {} rounds: total {}, checksum {}", count, n, rounds, total, checksum);
}
