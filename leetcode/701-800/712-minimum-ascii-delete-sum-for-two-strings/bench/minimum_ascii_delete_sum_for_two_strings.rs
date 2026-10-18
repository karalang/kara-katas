// LeetCode #712: Minimum ASCII Delete Sum for Two Strings -- a table
// of prefixes.
// Benchmark mirror of the Kara star arm: cost[i][j] is the least ASCII
// sum deleted to make the first i bytes of s1 equal to the first j of
// s2, in a table of rows allocated per call.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn minimum_delete_sum(s1: &str, s2: &str) -> i64 {
    let a = s1.as_bytes();
    let b = s2.as_bytes();
    let (m, n) = (a.len(), b.len());
    let mut cost: Vec<Vec<i64>> = Vec::new();
    for _ in 0..m + 1 {
        cost.push(vec![0; n + 1]);
    }
    for i in 1..m + 1 {
        cost[i][0] = cost[i - 1][0] + a[i - 1] as i64;
    }
    for j in 1..n + 1 {
        cost[0][j] = cost[0][j - 1] + b[j - 1] as i64;
    }
    for i in 1..m + 1 {
        for j in 1..n + 1 {
            if a[i - 1] == b[j - 1] {
                cost[i][j] = cost[i - 1][j - 1];
            } else {
                let drop_a = cost[i - 1][j] + a[i - 1] as i64;
                let drop_b = cost[i][j - 1] + b[j - 1] as i64;
                cost[i][j] = if drop_a < drop_b { drop_a } else { drop_b };
            }
        }
    }
    cost[m][n]
}

fn main() {
    let mut seed: i64 = 712;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..20 {
        let mut s = String::new();
        for _ in 0..1000 {
            s.push((97 + next_random(&mut seed) % 26) as u8 as char);
        }
        words.push(s);
    }
    let mut sum: i64 = 0;
    for _ in 0..10 {
        for p in 0..10 {
            sum += minimum_delete_sum(&words[2 * p], &words[2 * p + 1]);
        }
    }
    println!("10 rounds of 10 pairs of 1000 letters: sum {}", sum);
}
