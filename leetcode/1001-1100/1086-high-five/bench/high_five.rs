// Benchmark: LeetCode #1086 High Five -- mirrors high_five.kara: the
// scores grouped by student in a BTreeMap, each student's sorted high to
// low and the first five averaged, over 200 lists of 1000 items built
// once. The items are LeetCode's `Vec<Vec<i64>>`, as the Kāra arm's are.
use std::collections::BTreeMap;

fn high_five(items: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let mut scores: BTreeMap<i64, Vec<i64>> = BTreeMap::new();
    for item in items {
        match scores.get_mut(&item[0]) {
            Some(list) => list.push(item[1]),
            None => {
                scores.insert(item[0], vec![item[1]]);
            }
        }
    }
    let mut out = Vec::new();
    for (&id, list) in scores.iter() {
        let mut sorted = list.clone();
        sorted.sort_by(|a, b| b.cmp(a));
        let top: i64 = sorted.iter().take(5).sum();
        out.push(vec![id, top / 5]);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 50;
    let mut seed = 1086;
    let mut lists: Vec<Vec<Vec<i64>>> = Vec::new();
    for t in 0..200 {
        let k = 50 + t % 150;
        let mut ids: Vec<i64> = Vec::new();
        let mut taken = vec![false; 1001];
        while (ids.len() as i64) < k {
            let id = next_random(&mut seed) % 1000 + 1;
            if !taken[id as usize] {
                taken[id as usize] = true;
                ids.push(id);
            }
        }
        let mut items: Vec<Vec<i64>> = Vec::new();
        for i in 0..1000 {
            let id = if i < 5 * k { ids[(i % k) as usize] } else { ids[(next_random(&mut seed) % k) as usize] };
            items.push(vec![id, next_random(&mut seed) % 101]);
        }
        for i in (1..items.len()).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            items.swap(i, j);
        }
        lists.push(items);
    }
    let mut students: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..200 {
            let out = high_five(&lists[((r * 7 + i) % 200) as usize]);
            students += out.len() as i64;
            for row in out.iter() {
                check = (check * 31 + row[0] * 101 + row[1]) % 1000000007;
            }
        }
    }
    println!("{} rounds over 200 lists of 1000 items: {} students, checksum {}", rounds, students, check);
}
