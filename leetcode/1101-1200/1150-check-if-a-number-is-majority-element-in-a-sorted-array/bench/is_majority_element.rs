// LeetCode #1150: Check If a Number Is Majority Element in a Sorted Array
// -- the Rust mirror of the ★ arm: the run's start by `partition_point`,
// then the value n / 2 places on.

fn is_majority_element(nums: &[i64], target: i64) -> bool {
    let n = nums.len();
    let first = nums.partition_point(|&x| x < target);
    first + n / 2 < n && nums[first + n / 2] == target
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big(seed: &mut i64) -> i64 {
    (next_random(seed) * 32768 + next_random(seed)) % 1000000000 + 1
}

fn list(seed: &mut i64) -> Vec<i64> {
    let copies = (450 + next_random(seed) % 101) as usize;
    let v = big(seed);
    let mut nums = vec![v; copies];
    for _ in copies..1000 {
        nums.push(big(seed));
    }
    nums.sort();
    nums
}

fn main() {
    let mut seed = 1150;
    let lists: Vec<Vec<i64>> = (0..64).map(|_| list(&mut seed)).collect();
    let (mut yes, mut check) = (0i64, 0i64);
    for q in 0..10000000i64 {
        let nums = &lists[(q % 64) as usize];
        let kind = next_random(&mut seed) % 4;
        let target = if kind == 0 {
            nums[(next_random(&mut seed) % 1000) as usize]
        } else if kind == 1 {
            nums[500]
        } else if kind == 2 {
            nums[(next_random(&mut seed) % 1000) as usize] + 1
        } else {
            big(&mut seed)
        };
        if is_majority_element(nums, target) {
            yes += 1;
            check = (check * 31 + q) % 1000000007;
        }
    }
    println!("10000000 queries over 64 lists of 1000 values: majority {yes}, checksum {check}");
}
