// LeetCode #891 bench: the counting arm (a count of each value) on 400
// arrays of 100,000 numbers from 1 to 100,000. The same algorithm as
// sum_subseq_widths.kara.

const MODULUS: i64 = 1000000007;

fn sum_subseq_widths(nums: &[i64]) -> i64 {
    let n = nums.len();
    let largest = *nums.iter().max().unwrap() as usize;
    let mut count = vec![0usize; largest + 1];
    for &x in nums {
        count[x as usize] += 1;
    }
    let mut pow = vec![1i64; n + 1];
    for i in 1..n + 1 {
        pow[i] = pow[i - 1] * 2 % MODULUS;
    }
    let mut total = 0;
    let mut p = 0;
    for v in 0..largest + 1 {
        let c = count[v];
        if c > 0 {
            let block = pow[c] - 1;
            let as_max = pow[p] * block % MODULUS;
            let as_min = pow[n - p - c] * block % MODULUS;
            total = (total + v as i64 * (as_max - as_min)) % MODULUS;
            p += c;
        }
    }
    (total + MODULUS) % MODULUS
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 891;
    let mut sum = 0;
    let mut check = 0;
    for _ in 0..400 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            nums.push(1 + next_random(&mut seed) % 100000);
        }
        let got = sum_subseq_widths(&nums);
        sum = (sum + got) % MODULUS;
        check = (check * 131 + got) % MODULUS;
    }
    println!("400 arrays of 100000 numbers: widths sum to {}, checksum {}", sum, check);
}
