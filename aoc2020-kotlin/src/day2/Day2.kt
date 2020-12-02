package day2

import java.nio.file.Files
import java.nio.file.Paths

fun isValid1(n1: Int, n2: Int, char: Char, password: String): Boolean {
    val count = password.groupBy { it }.getOrDefault(char, emptyList()).size
    return count in n1..n2
}

fun isValid2(n1: Int, n2: Int, char: Char, password: String): Boolean {
    return (password[n1-1] == char) != (password[n2-1] == char)
}

fun countValid(lines: List<String>, isValid: (Int, Int, Char, String) -> Boolean): Int {
    val regex = """^([0-9]+)-([0-9]+) (.): (.*)$""".toRegex()
    return lines
            .asSequence()
            .map {regex.matchEntire(it.trim())}
            .filter {it != null}
            .map {it!!}
            .filter { mr: MatchResult ->
                isValid(mr.groupValues[1].toInt(), mr.groupValues[2].toInt(), mr.groupValues[3][0], mr.groupValues[4])
            }
            .count()
}

fun main() {
    val lines = Files.readAllLines(Paths.get("aoc2020/day2/input.txt"))
    println("Part 1: ${countValid(lines, ::isValid1)}")
    println("Part 2: ${countValid(lines, ::isValid2)}")
}