// LeetCode #682: Baseball Game -- a stack of the valid scores. Bench.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn cal_points(operations: &[String]) -> i64 {
    let mut record: Vec<i64> = Vec::new();
    for op in operations {
        if op == "+" {
            let n = record.len();
            record.push(record[n - 1] + record[n - 2]);
        } else if op == "D" {
            let n = record.len();
            record.push(record[n - 1] * 2);
        } else if op == "C" {
            record.pop();
        } else {
            record.push(op.parse::<i64>().unwrap());
        }
    }
    record.iter().sum()
}

fn random_ops(seed: &mut i64, n: usize) -> Vec<String> {
    let limit: i64 = 1073741824;
    let mut record: Vec<i64> = Vec::new();
    let mut out: Vec<String> = Vec::new();
    while out.len() < n {
        let k = record.len();
        let pick = next_random(seed) % 10;
        if pick == 0 && k >= 1 {
            record.pop();
            out.push("C".to_string());
        } else if pick == 1 && k >= 1 && record[k - 1].abs() < limit / 2 {
            record.push(record[k - 1] * 2);
            out.push("D".to_string());
        } else if pick == 2 && k >= 2 && (record[k - 1] + record[k - 2]).abs() < limit {
            record.push(record[k - 1] + record[k - 2]);
            out.push("+".to_string());
        } else if pick >= 3 {
            let x = next_random(seed) % 60001 - 30000;
            record.push(x);
            out.push(x.to_string());
        }
    }
    out
}

fn main() {
    let count: i64 = 200;
    let rounds: i64 = 30;
    let mut seed: i64 = 682;
    let lists: Vec<Vec<String>> = (0..count).map(|_| random_ops(&mut seed, 5000)).collect();
    let mut sum: i64 = 0;
    for r in 0..rounds {
        for k in 0..count {
            let at = (k * 7 + r) % count;
            let points = cal_points(&lists[at as usize]);
            sum = (sum * 31 + points % 1000000007 + 1000000007) % 1000000007;
        }
    }
    println!("{} games scored, checksum {}", count * rounds, sum);
}
