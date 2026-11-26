// LeetCode #1764: Form Array by Concatenating Subarrays of Another Array --
// the bench in Rust, mirroring can_choose.kara: greedy, each group matched
// at the first place it fits, compared value by value.
fn can_choose(groups: &[Vec<i32>], nums: &[i32]) -> bool {
    let mut at = 0;
    for group in groups {
        let len = group.len();
        loop {
            if at + len > nums.len() {
                return false;
            }
            if (0..len).all(|i| nums[at + i] == group[i]) {
                break;
            }
            at += 1;
        }
        at += len;
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_values(seed: &mut i64, n: i64, values: i64) -> Vec<i32> {
    (0..n).map(|_| (next_random(seed) % values) as i32).collect()
}

fn random_case(seed: &mut i64, k: i64, most: i64, values: i64, gap: i64, break_one: bool) -> (Vec<Vec<i32>>, Vec<i32>) {
    let mut groups: Vec<Vec<i32>> = Vec::new();
    let mut nums: Vec<i32> = Vec::new();
    for _ in 0..k {
        let filler = next_random(seed) % (gap + 1);
        nums.extend(random_values(seed, filler, values));
        let len = 1 + next_random(seed) % most;
        let group = random_values(seed, len, values);
        nums.extend(group.iter().copied());
        groups.push(group);
    }
    if break_one {
        let g = (next_random(seed) % k) as usize;
        let at = (next_random(seed) % groups[g].len() as i64) as usize;
        groups[g][at] = (next_random(seed) % values) as i32;
    }
    (groups, nums)
}

fn main() {
    let mut seed: i64 = 1764;
    let cases: Vec<(Vec<Vec<i32>>, Vec<i32>)> = (0..200).map(|i| random_case(&mut seed, 10, 40, 2, 60, i % 2 == 1)).collect();
    let mut check: i64 = 0;
    for call in 0..200000i64 {
        let c = &cases[((check + call * 7919) % 200) as usize];
        check = (check * 31 + if can_choose(&c.0, &c.1) { 1 } else { 0 } + call % 7) % 1000000007;
    }
    println!("200000 calls over 200 cases: checksum {}", check);
}
