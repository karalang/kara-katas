// Benchmark for #581: Rust mirror of the ★ arm (two sweeps); see
// find_unsorted_subarray.kara.

fn find_unsorted_subarray(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut largest = nums[0];
    let mut end: i64 = -1;
    for i in 1..n {
        if nums[i] < largest {
            end = i as i64;
        } else {
            largest = nums[i];
        }
    }
    let mut smallest = nums[n - 1];
    let mut start: i64 = 0;
    for i in (0..n - 1).rev() {
        if nums[i] > smallest {
            start = i as i64;
        } else {
            smallest = nums[i];
        }
    }
    if end == -1 {
        0
    } else {
        end - start + 1
    }
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed) * 32768;
    high + next_random(seed)
}

fn main() {
    let count: i64 = 100;
    let rounds: i64 = 600;
    let mut seed: i64 = 581;
    let mut cases: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..10000 {
            nums.push(wide(&mut seed) % 200001 - 100000);
        }
        nums.sort();
        let swaps = 1 + next_random(&mut seed) % 3;
        for _ in 0..swaps {
            let i = (wide(&mut seed) % 10000) as usize;
            let j = (wide(&mut seed) % 10000) as usize;
            nums.swap(i, j);
        }
        cases.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let p = ((round * 7 + g) % count) as usize;
            let got = find_unsorted_subarray(&cases[p]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} arrays of 10000 values, {} rounds: total {}, checksum {}", count, rounds, total, checksum);
}
