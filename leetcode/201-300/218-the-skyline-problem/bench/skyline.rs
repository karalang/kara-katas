#[derive(Clone, Copy)]
struct Building {
    left: i64,
    right: i64,
    height: i64,
}

#[derive(Clone, Copy)]
struct Point {
    x: i64,
    h: i64,
}

fn merge(left: &[Point], right: &[Point]) -> Vec<Point> {
    let mut result: Vec<Point> = Vec::new();
    let nl = left.len() as i64;
    let nr = right.len() as i64;
    let mut i = 0i64;
    let mut j = 0i64;
    let mut h1 = 0i64;
    let mut h2 = 0i64;
    while i < nl && j < nr {
        let x;
        if left[i as usize].x < right[j as usize].x {
            x = left[i as usize].x;
            h1 = left[i as usize].h;
            i += 1;
        } else if left[i as usize].x > right[j as usize].x {
            x = right[j as usize].x;
            h2 = right[j as usize].h;
            j += 1;
        } else {
            x = left[i as usize].x;
            h1 = left[i as usize].h;
            h2 = right[j as usize].h;
            i += 1;
            j += 1;
        }
        let maxh = if h1 > h2 { h1 } else { h2 };
        if result.is_empty() || result[result.len() - 1].h != maxh {
            result.push(Point { x, h: maxh });
        }
    }
    while i < nl {
        result.push(left[i as usize]);
        i += 1;
    }
    while j < nr {
        result.push(right[j as usize]);
        j += 1;
    }
    result
}

fn skyline(bs: &[Building], lo: i64, hi: i64) -> Vec<Point> {
    if hi - lo == 1 {
        let b = bs[lo as usize];
        return vec![Point { x: b.left, h: b.height }, Point { x: b.right, h: 0 }];
    }
    let mid = lo + (hi - lo) / 2;
    let left = skyline(bs, lo, mid);
    let right = skyline(bs, mid, hi);
    merge(&left, &right)
}

fn main() {
    let n: i64 = 24000;
    let passes: i64 = 100;
    let xr: i64 = 200000;
    let wr: i64 = 120;
    let hr: i64 = 1000;

    let mut bs: Vec<Building> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let left = state % xr;
        state = (state * 1103515245 + 12345) & 2147483647;
        let width = 1 + state % wr;
        state = (state * 1103515245 + 12345) & 2147483647;
        let height = 1 + state % hr;
        bs.push(Building { left, right: left + width, height });
    }

    let mut sink: i64 = 0;
    for p in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let idx = (p % n) as usize;
        bs[idx].height = 1 + state % hr;
        let sky = skyline(&bs, 0, n);
        for pt in &sky {
            sink += pt.x + pt.h;
        }
    }
    println!("{}", sink);
}
