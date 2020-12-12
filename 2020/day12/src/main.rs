use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

struct AOCProcessor {
    input: String,
    instructions: Vec<String>,
    result_a: i32,
    result_b: i32,
}

impl AOCProcessor {
    pub fn new(input: String) -> AOCProcessor {
        AOCProcessor {
            input,
            instructions: Vec::new(),
            result_a: 0,
            result_b: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();

        let _ = match File::open(&self.input) {
            Ok(file) => {
                for line in io::BufReader::new(file).lines() {
                    if let Ok(line) = line {
                        self.process_line(&line[..]);
                    }
                }
            }
            Err(error) => return Err(error),
        };

        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {
        self.instructions.clear();
    }

    pub fn finalize(&mut self) {
        let save_instructions = self.instructions.clone();
        self.finalize_a();
        self.instructions = save_instructions;
        self.finalize_b();
    }

    fn process_line(&mut self, line: &str) {
        if line.len() > 0 {
            self.instructions.push(String::from(line));
        }
    }

    fn finalize_a(&mut self) {
        let mut ship_x = 0;
        let mut ship_y = 0;
        let mut ship_direction: f64 = 90.0;

        if AOCDEBUG {
            println!("({}, {}, {})", ship_x, ship_y, ship_direction);
        }
        for line in self.instructions.iter() {
            let op = String::from(&line[0..1]).parse::<char>().unwrap();
            let arg = String::from(&line[1..]).parse::<i32>().unwrap();
            match op {
                'N' => {
                    ship_y += arg;
                }
                'S' => {
                    ship_y -= arg;
                }
                'E' => {
                    ship_x += arg;
                }
                'W' => {
                    ship_x -= arg;
                }
                'R' => {
                    ship_direction = (ship_direction + arg as f64) % 360.0;
                }
                'L' => {
                    ship_direction = (ship_direction + 360.0 - arg as f64) % 360.0;
                }
                'F' => {
                    ship_x += ship_direction.to_radians().sin() as i32 * arg;
                    ship_y += ship_direction.to_radians().cos() as i32 * arg;
                }
                _ => {}
            }
            if AOCDEBUG {
                println!(
                    "{} {} -> ({}, {}, {})",
                    op, arg, ship_x, ship_y, ship_direction
                );
            }
        }
        self.result_a = ship_x.abs() + ship_y.abs();
        println!("result_a:{}", self.result_a);
    }

    fn finalize_b(&mut self) {
        let mut ship_x = 0;
        let mut ship_y = 0;
        let mut wp_x = 10;
        let mut wp_y = 1;

        if AOCDEBUG {
            println!("({}, {}) : ({}, {})", ship_x, ship_y, wp_x, wp_y);
        }
        for line in self.instructions.iter() {
            let op = String::from(&line[0..1]).parse::<char>().unwrap();
            let arg = String::from(&line[1..]).parse::<i32>().unwrap();
            match op {
                'N' => {
                    wp_y += arg;
                }
                'S' => {
                    wp_y -= arg;
                }
                'E' => {
                    wp_x += arg;
                }
                'W' => {
                    wp_x -= arg;
                }
                'R' => {
                    let c = (360.0 - arg as f64).to_radians().cos();
                    let s = (360.0 - arg as f64).to_radians().sin();
                    let nx = (wp_x as f64 * c - wp_y as f64 * s).round();
                    let ny = (wp_x as f64 * s + wp_y as f64 * c).round();
                    wp_x = nx as i32;
                    wp_y = ny as i32;
                }
                'L' => {
                    let c = (arg as f64).to_radians().cos();
                    let s = (arg as f64).to_radians().sin();
                    let nx = (wp_x as f64 * c - wp_y as f64 * s).round();
                    let ny = (wp_x as f64 * s + wp_y as f64 * c).round();
                    wp_x = nx as i32;
                    wp_y = ny as i32;
                }
                'F' => {
                    ship_x += arg * wp_x;
                    ship_y += arg * wp_y;
                }
                _ => {}
            }
            if AOCDEBUG {
                println!(
                    "{} {} -> ({}, {}) : ({}, {})",
                    op, arg, ship_x, ship_y, wp_x, wp_y
                );
            }
        }
        self.result_b = ship_x.abs() + ship_y.abs();
        println!("result_b:{}", self.result_b);
    }
}

fn main() {
    let mut processor = AOCProcessor::new(String::from("input.txt"));
    match processor.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
