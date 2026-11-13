// LeetCode #1146: Snapshot Array -- the Rust mirror of the ★ arm: a
// history of (snap, value) pairs for each place, the last pair at or
// before the snap asked found with `partition_point`.

struct SnapshotArray {
    history: Vec<Vec<(i64, i64)>>,
    snaps: i64,
}

impl SnapshotArray {
    fn new(length: usize) -> Self {
        SnapshotArray { history: vec![vec![(0, 0)]; length], snaps: 0 }
    }

    fn set(&mut self, index: usize, val: i64) {
        let h = &mut self.history[index];
        let last = h.len() - 1;
        if h[last].0 == self.snaps {
            h[last].1 = val;
        } else {
            h.push((self.snaps, val));
        }
    }

    fn snap(&mut self) -> i64 {
        self.snaps += 1;
        self.snaps - 1
    }

    fn get(&self, index: usize, snap_id: i64) -> i64 {
        let h = &self.history[index];
        h[h.partition_point(|&(s, _)| s <= snap_id) - 1].1
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let n = 50000;
    let mut arr = SnapshotArray::new(n as usize);
    let mut seed = 1146;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..50000i64 {
        for _ in 0..50 {
            let i = wide(&mut seed) % n;
            let v = wide(&mut seed) % 1000000001;
            arr.set(i as usize, v);
        }
        arr.snap();
        for _ in 0..50 {
            let i = wide(&mut seed) % n;
            let s = wide(&mut seed) % (r + 1);
            let got = arr.get(i as usize, s);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("50000 rounds of 50 sets, a snap and 50 gets on 50000 places: gets total {total}, checksum {check}");
}
