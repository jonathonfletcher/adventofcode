use std::fs::File;
use std::io::{self, BufRead};
use std::vec::Vec;

fn process_line(line: &str) -> (i32, i32) {
    let mut row_val: i32 = 64;
    let mut seat_val: i32 = 4;
    let mut row = 0;
    let mut seat = 0;
    for v in line.chars() {
        match v {
            'F' => {
                row_val /= 2;
            },
            'B' => {
                row += row_val;
                row_val /= 2;
            },
            'L' => {
                seat_val /= 2;
            },
            'R' => {
                seat += seat_val;
                seat_val /= 2;
            },
            _ => {
                panic!("{}", v);
            }
        }
    }
    (row as i32, seat as i32)
}

fn main() {

    let mut grid: Vec<Vec<i32>> = Vec::new();

    let file = match File::open("input.txt") {
        Ok(file) => file,
        Err(error) => panic!("{}", error)
    };

    for y in (0..127) {
        grid.push(vec![0, 0, 0, 0, 0, 0, 0, 0]);
    }
    println!("{:?}", grid);

    let mut max_score = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line) = line {
            if line.len() > 0 {
                let (row, seat) = process_line(&line);
                let score = row * 8 + seat;
                if score > max_score {
                    max_score = score;
                }
                grid[row as usize][seat as usize] = 1;
            }
        }
    }
    println!("max_score: {}", max_score);
    let mut passed_front = false;
    for y in (0..grid.len()) {
        let mut row_count = 0;
        for x in (0..8) {
            if grid[y][x] == 0 {
                if passed_front {
                    println!("{}", y*8+x);
                    break;
                }
            } else {
                row_count += 1;
            }
        }
        if !passed_front {
            if row_count == 8 {
                passed_front = true;
            }
        }
    }
}
