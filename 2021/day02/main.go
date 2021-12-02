package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

func part1(scanner *bufio.Scanner) int64 {

	var posX int64 = 0
	var posY int64 = 0
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(line, " ")
		if len(parts) == 2 {
			var moveDirection string = parts[0]
			moveSize, _ := strconv.ParseInt(parts[1], 10, 32)
			switch moveDirection {
			case "forward":
				posX += moveSize
			case "down":
				posY += moveSize
			case "up":
				posY -= moveSize
			default:
				log.Fatal(line)
			}
		} else {
			log.Fatal(line)
		}
		// log.Println(posX, posY)
	}

	return posX * posY
}

func part2(scanner *bufio.Scanner) int64 {

	var posX int64 = 0
	var posY int64 = 0
	var posAim int64 = 0
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(line, " ")
		if len(parts) == 2 {
			var moveDirection string = parts[0]
			moveSize, _ := strconv.ParseInt(parts[1], 10, 32)
			switch moveDirection {
			case "forward":
				posX += moveSize
				posY += posAim * moveSize
			case "down":
				posAim += moveSize
			case "up":
				posAim -= moveSize
			default:
				log.Fatal(line)
			}
		} else {
			log.Fatal(line)
		}
		// log.Println(posX, posY)
	}

	return posX * posY
}

func main() {

	{
		inFile, err := os.Open("part1.txt")
		if err != nil {
			log.Fatal("cannot open input")
		} else {
			scanner := bufio.NewScanner(inFile)
			scanner.Split(bufio.ScanLines)
			partAnswer := part1(scanner)
			log.Println("part1:", partAnswer)
			inFile.Close()
		}
	}

	{
		inFile, err := os.Open("part1.txt")
		if err != nil {
			log.Fatal("cannot open input")
		} else {
			scanner := bufio.NewScanner(inFile)
			scanner.Split(bufio.ScanLines)
			partAnswer := part2(scanner)
			log.Println("part2:", partAnswer)
			inFile.Close()
		}
	}

}
