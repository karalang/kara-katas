// LeetCode 749 — Contain Virus, bench: the ★ arm (flood fill each day)
// on a 50 x 50 grid that keeps changing. Mirrors contain_virus.kara.

fn contain_virus(is_infected: &[Vec<i64>]) -> i64 {
    let m = is_infected.len();
    let n = is_infected[0].len();
    // 0 clean, 1 infected, 2 walled off
    let mut g: Vec<i64> = is_infected.iter().flatten().copied().collect();
    let mut walls = 0;
    loop {
        let mut region = vec![usize::MAX; m * n];
        let mut mark = vec![usize::MAX; m * n];
        let mut cells: Vec<Vec<usize>> = Vec::new();
        let mut threats: Vec<Vec<usize>> = Vec::new();
        let mut needs: Vec<i64> = Vec::new();
        for start in 0..m * n {
            if g[start] != 1 || region[start] != usize::MAX {
                continue;
            }
            let id = cells.len();
            let mut mine = Vec::new();
            let mut threat = Vec::new();
            let mut need = 0;
            let mut stack = vec![start];
            region[start] = id;
            while let Some(at) = stack.pop() {
                mine.push(at);
                let (r, c) = (at / n, at % n);
                let mut next = Vec::new();
                if r > 0 {
                    next.push(at - n);
                }
                if r < m - 1 {
                    next.push(at + n);
                }
                if c > 0 {
                    next.push(at - 1);
                }
                if c < n - 1 {
                    next.push(at + 1);
                }
                for &y in &next {
                    if g[y] == 0 {
                        need += 1;
                        if mark[y] != id {
                            mark[y] = id;
                            threat.push(y);
                        }
                    } else if g[y] == 1 && region[y] == usize::MAX {
                        region[y] = id;
                        stack.push(y);
                    }
                }
            }
            cells.push(mine);
            threats.push(threat);
            needs.push(need);
        }
        let mut best: Option<usize> = None;
        for id in 0..cells.len() {
            if !threats[id].is_empty() && best.map_or(true, |b| threats[id].len() > threats[b].len()) {
                best = Some(id);
            }
        }
        let Some(best) = best else { break };
        walls += needs[best];
        for id in 0..cells.len() {
            if id == best {
                for &x in &cells[id] {
                    g[x] = 2;
                }
            } else {
                for &x in &threats[id] {
                    g[x] = 1;
                }
            }
        }
    }
    walls
}

struct Rng(i64);
impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let rounds = 3000;
    let mut rng = Rng(749);
    let mut grid: Vec<Vec<i64>> = (0..50)
        .map(|_| (0..50).map(|_| if rng.next() % 100 < 5 { 1 } else { 0 }).collect())
        .collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for _ in 0..20 {
            let r = (rng.next() % 50) as usize;
            let c = (rng.next() % 50) as usize;
            grid[r][c] = if rng.next() % 100 < 5 { 1 } else { 0 };
        }
        let w = contain_virus(&grid);
        total += w;
        check = (check * 31 + w) % 1000000007;
    }
    println!("{} grids of 50 x 50: {} walls in all, checksum {}", rounds, total, check);
}
