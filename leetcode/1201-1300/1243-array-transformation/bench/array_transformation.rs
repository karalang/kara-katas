// LeetCode #1243: the benchmark, mirroring the Kāra file.

fn transform_array(arr: Vec<i64>) -> Vec<i64> {
    let mut cur = arr;
    loop {
        let mut next = cur.clone();
        for i in 1..cur.len() - 1 {
            if cur[i] < cur[i - 1] && cur[i] < cur[i + 1] {
                next[i] += 1;
            } else if cur[i] > cur[i - 1] && cur[i] > cur[i + 1] {
                next[i] -= 1;
            }
        }
        if next == cur {
            return cur;
        }
        cur = next;
    }
}

fn main() {
    let mut seed: i64 = 1243;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..5000 {
        arrays.push(
            (0..100)
                .map(|_| {
                    seed = (seed * 1103515245 + 12345) % 2147483648;
                    seed / 65536 % 100 + 1
                })
                .collect(),
        );
    }
    let mut check: i64 = 0;
    for _ in 0..10 {
        for a in &arrays {
            for v in transform_array(a.clone()) {
                check = (check * 131 + v) % 1000000007;
            }
        }
    }
    println!("10 rounds of 5000 arrays of 100 values: checksum {check}");
}
