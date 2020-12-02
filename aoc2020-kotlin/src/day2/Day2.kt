package day2

import java.nio.file.Files
import java.nio.file.Paths

fun isValid1(n1: Int, n2: Int, char: Char, password: String): Boolean {
    return (password.count { it == char }) in n1..n2
}

fun isValid2(n1: Int, n2: Int, char: Char, password: String): Boolean {
    return (password[n1 - 1] == char) xor (password[n2 - 1] == char)
}

fun countValid(lines: List<String>, isValid: (Int, Int, Char, String) -> Boolean): Int {
    val regex = """^(\d+)-(\d+) (.): (.*)$""".toRegex()
    return lines
            .mapNotNull { regex.matchEntire(it.trim()) }
            .count {
                isValid(it.groupValues[1].toInt(), it.groupValues[2].toInt(), it.groupValues[3][0], it.groupValues[4])
            }
}

fun main() {
    val lines = Files.readAllLines(Paths.get("aoc2020/day2/input.txt"))
    println("Part 1: ${countValid(lines, ::isValid1)}")
    println("Part 2: ${countValid(lines, ::isValid2)}")
}