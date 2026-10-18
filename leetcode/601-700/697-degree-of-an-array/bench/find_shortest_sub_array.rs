// LeetCode #697: Degree of an Array -- bench program, Rust mirror of the table arm.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn find_shortest_sub_array(nums: &[i64]) -> i64 {
    let size = 50000;
    let mut count: Vec<i64> = vec![0; size];
    let mut first: Vec<i64> = vec![-1; size];
    let mut last: Vec<i64> = vec![0; size];
    for i in 0..nums.len() {
        let x = nums[i] as usize;
        if first[x] < 0 {
            first[x] = i as i64;
        }
        last[x] = i as i64;
        count[x] += 1;
    }
    let mut degree = 0;
    let mut best = nums.len() as i64;
    for x in 0..size {
        if count[x] == 0 {
            continue;
        }
        let span = last[x] - first[x] + 1;
        if count[x] > degree || (count[x] == degree && span < best) {
            degree = count[x];
            best = span;
        }
    }
    best
}

fn main() {
    let mut seed = 697;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for k in 0..40 {
        let range = 1 + 1250 * k;
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..50000 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            nums.push((a * 65536 + b) % range);
        }
        arrays.push(nums);
    }
    let rounds = 20;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for nums in &arrays {
            let r = find_shortest_sub_array(nums);
            total += r;
            checksum = (checksum * 31 + r) % 1000000007;
        }
    }
    println!("{} rounds of 40 arrays of 50000: shortest spans sum to {}, checksum {}", rounds, total, checksum);
}
