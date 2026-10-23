// LeetCode #923: 3Sum With Multiplicity -- bench: counting the values.
// Mirrors three_sum_multi.kara.

fn three_sum_multi(arr: &[i64], target: i64) -> i64 {
    let modulus = 1000000007;
    let mut count = [0i64; 101];
    for &v in arr {
        count[v as usize] += 1;
    }
    let mut total = 0;
    for x in 0..101usize {
        if 3 * x as i64 > target {
            break;
        }
        for y in x..101usize {
            let z = target - x as i64 - y as i64;
            if z < y as i64 {
                break;
            }
            if z > 100 {
                continue;
            }
            let z = z as usize;
            let ways = if x == y && y == z {
                count[x] * (count[x] - 1) * (count[x] - 2) / 6
            } else if x == y {
                count[x] * (count[x] - 1) / 2 * count[z]
            } else if y == z {
                count[x] * count[y] * (count[y] - 1) / 2
            } else {
                count[x] * count[y] * count[z]
            };
            total = (total + ways) % modulus;
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n) = (500i64, 100i64, 3000);
    let mut seed = 923;
    // count arrays of n values from 0 to 100, built once
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let arr: Vec<i64> = (0..n).map(|_| next_random(&mut seed) % 101).collect();
        arrays.push(arr);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round asks every array for a different target up to 300
        for i in 0..count {
            let a = three_sum_multi(&arrays[i as usize], (r * 7 + i) % 301);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds over {count} arrays of {n}: answers summing to {total}, checksum {check}"
    );
}
