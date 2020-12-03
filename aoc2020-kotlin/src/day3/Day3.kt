package day3

import java.nio.file.Files
import java.nio.file.Paths

fun countTrees(grid: List<String>, right: Int, down: Int): Int {
    val width = grid[0].length
    return (grid.indices step down).count { y ->
        val x = y / down * right
        grid[y][x % width] == '#'
    }
}


fun main() {
    val grid = Files.readAllLines(Paths.get("aoc2020/day3/input.txt"))

    println("Part 1: ${countTrees(grid, 3, 1)}")

    val answer = listOf(Pair(1, 1), Pair(3, 1), Pair(5, 1), Pair(7, 1), Pair(1, 2))
            .map { (x, y) -> countTrees(grid, x, y) }
            .reduce { x, y -> x * y }
    println("Part 2: $answer")
}