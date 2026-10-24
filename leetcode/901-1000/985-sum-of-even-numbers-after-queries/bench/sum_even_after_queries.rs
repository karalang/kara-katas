// Benchmark: LeetCode #985 Sum of Even Numbers After Queries -- the ★ arm, a
// running sum, on LeetCode's largest: 10000 values and 10000 queries.
// Mirrors sum_even_after_queries.kara, .c, .py and go-seq/.

fn sum_even_after_queries(nums: &[i64], queries: &[(i64, i64)]) -> Vec<i64> {
    let mut a = nums.to_vec();
    let mut even = 0;
    for &x in a.iter() {
        if x % 2 == 0 {
            even += x;
        }
    }
    let mut answer = Vec::new();
    for &(val, index) in queries {
        let index = index as usize;
        if a[index] % 2 == 0 {
            even -= a[index];
        }
        a[index] += val;
        if a[index] % 2 == 0 {
            even += a[index];
        }
        answer.push(even);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 300;
    let mut seed = 985;
    let mut cases: Vec<(Vec<i64>, Vec<(i64, i64)>)> = Vec::new();
    for _ in 0..20 {
        let mut nums = Vec::new();
        for _ in 0..10000 {
            nums.push(next_random(&mut seed) % 20001 - 10000);
        }
        let mut queries = Vec::new();
        for _ in 0..10000 {
            let val = next_random(&mut seed) % 20001 - 10000;
            queries.push((val, next_random(&mut seed) % 10000));
        }
        cases.push((nums, queries));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let (nums, queries) = &cases[(r + i) % 20];
            let answer = sum_even_after_queries(nums, queries);
            let last = answer[answer.len() - 1];
            total += last;
            check = (check * 31 + (last % 1000000007 + 1000000007) % 1000000007) % 1000000007;
        }
    }
    println!("{} rounds over 20 cases of 10000 values and 10000 queries: sum {}, checksum {}", rounds, total, check);
}
