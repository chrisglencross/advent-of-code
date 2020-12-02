package day1

import aocutil.combinations
import java.nio.file.Files
import java.nio.file.Paths

fun main() {

    fun solve(values: List<Int>, select: Int): List<Int> {
        return combinations(values, select)
                .filter { it.sum() == 2020 }
                .map { it.reduce { x, y -> x * y } }
                .toList()
    }

    val lines = Files.readAllLines(Paths.get("aoc2020/day1/input.txt"))
    val values = lines.map { it.toInt() }

    println(solve(values, 2))
    println(solve(values, 3))
}