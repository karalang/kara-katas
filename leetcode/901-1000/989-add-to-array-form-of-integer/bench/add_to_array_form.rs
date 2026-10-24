// LeetCode #989: Add to Array-Form of Integer -- bench, the ★ arm
// (k carried in from the last digit), the same algorithm and workload
// as add_to_array_form.kara.

fn add_to_array_form(num: &[i64], k: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut carry = k;
    let mut i = num.len() as i64 - 1;
    while i >= 0 || carry > 0 {
        if i >= 0 {
            carry += num[i as usize];
            i -= 1;
        }
        out.push(carry % 10);
        carry /= 10;
    }
    out.reverse();
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_num(n: usize, seed: &mut i64) -> Vec<i64> {
    let mut out = Vec::new();
    for i in 0..n {
        let mut d = next_random(seed) % 10;
        if i == 0 && d == 0 {
            d = 1;
        }
        out.push(d);
    }
    out
}

fn main() {
    let rounds = 1000;
    let mut seed = 989;
    let nums: Vec<Vec<i64>> = (0..20).map(|_| random_num(10000, &mut seed)).collect();
    let mut digits = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let k = 1 + next_random(&mut seed) % 10000;
            let got = add_to_array_form(&nums[(r + i) % 20], k);
            digits += got.len();
            for j in got.len() - 6..got.len() {
                check = (check * 31 + got[j] + 1) % 1000000007;
            }
        }
    }
    println!("{} rounds over 20 numbers of 10000 digits: {} digits out, checksum {}", rounds, digits, check);
}
