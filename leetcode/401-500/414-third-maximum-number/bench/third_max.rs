// LeetCode #414: Third Maximum Number -- Rust mirror of third_max.kara
// (three slots).

fn third_max(nums: &[i64]) -> i64 {
    let mut first: Option<i64> = None;
    let mut second: Option<i64> = None;
    let mut third: Option<i64> = None;
    for &x in nums {
        if first == Some(x) || second == Some(x) || third == Some(x) {
            continue;
        }
        match first {
            None => {
                first = Some(x);
                continue;
            }
            Some(a) => {
                if x > a {
                    third = second;
                    second = first;
                    first = Some(x);
                    continue;
                }
            }
        }
        match second {
            None => {
                second = Some(x);
                continue;
            }
            Some(b) => {
                if x > b {
                    third = second;
                    second = Some(x);
                    continue;
                }
            }
        }
        match third {
            None => third = Some(x),
            Some(c) => {
                if x > c {
                    third = Some(x);
                }
            }
        }
    }
    match third {
        Some(c) => c,
        None => first.unwrap(),
    }
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn value(seed: &mut i64) -> i64 {
    let high = step(seed);
    let low = step(seed);
    high * 131072 + low * 4 - 2147483648
}

fn main() {
    let n: i64 = 10000;
    let rounds: i64 = 50000;
    let mut seed: i64 = 414;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(value(&mut seed));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        nums[(r * 7919 % n) as usize] = value(&mut seed);
        let answer = third_max(&nums);
        total += answer;
        checksum = (checksum * 31 + answer % 1000000007 + 1000000007) % 1000000007;
    }
    println!("{rounds} rounds on {n} numbers: total {total}, checksum {checksum}");
}
