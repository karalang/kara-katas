// LeetCode #2172: Maximum AND Sum of Array -- the benchmark's Rust mirror
// of and_sum.kara.

fn maximum_and_sum(nums: &[i64], num_slots: i64) -> i64 {
    let mut powers: Vec<i64> = Vec::new();
    let mut p = 1i64;
    for _ in 0..num_slots {
        powers.push(p);
        p *= 3;
    }
    let mut best: Vec<i64> = vec![-1; p as usize];
    best[0] = 0;
    let mut answer = 0i64;
    for fill in 0..p {
        if best[fill as usize] < 0 {
            continue;
        }
        let mut placed = 0i64;
        let mut rest = fill;
        while rest > 0 {
            placed += rest % 3;
            rest /= 3;
        }
        if placed == nums.len() as i64 {
            answer = answer.max(best[fill as usize]);
            continue;
        }
        for slot in 0..num_slots {
            if fill / powers[slot as usize] % 3 < 2 {
                let next = (fill + powers[slot as usize]) as usize;
                let sum = best[fill as usize] + (nums[placed as usize] & (slot + 1));
                if sum > best[next] {
                    best[next] = sum;
                }
            }
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2172i64;
    let mut row: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        row.push(next_random(&mut seed) % 15 + 1);
    }
    let mut check = 0i64;
    for _ in 0..200 {
        let start = (next_random(&mut seed) % 99983) as usize;
        let best = maximum_and_sum(&row[start..start + 18], 9);
        check = (check * 31 + best) % 1000000007;
    }
    println!("200 solves: checksum {}", check);
}
