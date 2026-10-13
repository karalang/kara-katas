// Benchmark for #540: Rust mirror of the ★ arm (binary search over the
// pairs); see single_non_duplicate.kara.

fn single_non_duplicate(nums: &[i64]) -> i64 {
    let mut low = 0;
    let mut high = nums.len() - 1;
    while low < high {
        let mut mid = (low + high) / 2;
        if mid % 2 == 1 {
            mid -= 1;
        }
        if nums[mid] == nums[mid + 1] {
            low = mid + 2;
        } else {
            high = mid;
        }
    }
    nums[low]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 100 arrays of 0 to 49,999 pairs and the single element at a
    // random place, values rising by 1 or 2, built once. Then the answer
    // for each array is found 200,000 times.
    let arrays = 100;
    let mut seed: i64 = 540;
    let mut all: Vec<Vec<i64>> = Vec::new();
    let mut elements = 0;
    for _ in 0..arrays {
        let high = next_random(&mut seed);
        let pairs = (high * 32768 + next_random(&mut seed)) % 50000;
        let high = next_random(&mut seed);
        let single = (high * 32768 + next_random(&mut seed)) % (pairs + 1);
        let mut nums = Vec::new();
        let mut v = 0;
        for i in 0..pairs + 1 {
            v += 1 + next_random(&mut seed) % 2;
            nums.push(v);
            if i != single {
                nums.push(v);
            }
        }
        elements += nums.len();
        all.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..200000 {
        for nums in &all {
            let answer = single_non_duplicate(nums);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    println!("{arrays} arrays, {elements} elements, 200000 times each: total {total}, checksum {checksum}");
}
