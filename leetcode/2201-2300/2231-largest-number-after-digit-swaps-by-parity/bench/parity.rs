// LeetCode #2231: Largest Number After Digit Swaps by Parity -- the
// benchmark's Rust mirror of parity.kara: each parity's digits sorted
// from largest down into that parity's places.

fn largest_integer(num: i64) -> i64 {
    let digits: Vec<i64> = num.to_string().chars().map(|c| c as i64 - 48).collect();
    let mut odd: Vec<i64> = Vec::new();
    let mut even: Vec<i64> = Vec::new();
    for &d in &digits {
        if d % 2 == 1 {
            odd.push(d);
        } else {
            even.push(d);
        }
    }
    odd.sort();
    even.sort();
    let mut largest = 0;
    for &d in &digits {
        let next = if d % 2 == 1 { odd.pop().unwrap() } else { even.pop().unwrap() };
        largest = largest * 10 + next;
    }
    largest
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2231;
    let mut nums: Vec<i64> = (0..100000).map(|_| wide_random(&mut seed) % 1000000000 + 1).collect();
    let mut check: i64 = 0;
    for _ in 0..20 {
        // punch: one num drawn again before each pass over all of them
        let at = (wide_random(&mut seed) % 100000) as usize;
        nums[at] = wide_random(&mut seed) % 1000000000 + 1;
        for &num in &nums {
            check = (check * 31 + largest_integer(num)) % 1000000007;
        }
    }
    println!("20 passes over 10^5 nums: checksum {check}");
}
