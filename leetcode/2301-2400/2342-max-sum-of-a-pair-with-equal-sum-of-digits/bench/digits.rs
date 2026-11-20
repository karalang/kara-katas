// LeetCode #2342: Max Sum of a Pair With Equal Sum of Digits -- the bench,
// the ★ arm in Rust: a table of 82 keeping the largest value seen for each
// digit sum, each value paired with the largest before it of its own sum.

fn digit_sum(x: i64) -> i64 {
    let mut rest = x;
    let mut s = 0;
    while rest > 0 {
        s += rest % 10;
        rest /= 10;
    }
    s
}

fn maximum_sum(nums: &[i64]) -> i64 {
    let mut best = vec![-1i64; 82];
    let mut answer = -1;
    for &x in nums {
        let s = digit_sum(x) as usize;
        if best[s] >= 0 {
            answer = answer.max(best[s] + x);
        }
        best[s] = best[s].max(x);
    }
    answer
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let arrays: Vec<Vec<i64>> = (0..10i64)
        .map(|a| (0..100000i64).map(|i| scrambled(a * 100000 + i) % 1000000000 + 1).collect())
        .collect();
    let mut check = 0i64;
    for p in 0..20i64 {
        for nums in &arrays {
            check = (check * 31 + maximum_sum(nums) + p) % 1000000007;
        }
    }
    println!("20 passes over 10 arrays of 10^5 values: checksum {}", check);
}
