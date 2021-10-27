import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Reimplementation of the subroutine at address 6027 in Java, with memoization.
 * <p>
 * About 10x faster than the Python version which makes it more suitable for brute forcing the correct value of r7.
 */
public class FindR7 {

    private final Map<List<Integer>, List<Integer>> memo = new LinkedHashMap<>();

    private int r0;
    private int r1;
    private final int r7;

    public FindR7(int r7) {
        this.r7 = r7;
    }

    private void fn6027() {

        List<Integer> inRegisters = List.of(r0, r1);
        List<Integer> outRegisters = memo.get(inRegisters);
        if (outRegisters != null) {
            this.r0 = outRegisters.get(0);
            this.r1 = outRegisters.get(1);
            return;
        }

        if (r0 == 0) {
            r0 = (r1 + 1) % 32768;
        } else if (r1 == 0) {
            r0--;
            r1 = r7;
            fn6027();
        } else {
            int t = r0;
            r1--;
            fn6027();
            r1 = r0;
            r0 = t;
            r0--;
            fn6027();
        }

        outRegisters = List.of(r0, r1, r7);
        memo.put(inRegisters, outRegisters);
    }

    public void warmCache() {
        for (int r0 = 0; r0 < 5; r0++) {
            for (int r1 = 0; r1 < 32768; r1++) {
                this.r0 = r0;
                this.r1 = r1;
                fn6027();
            }
        }
    }

    public static void main(String[] args) {
        for (int r7 = 0; r7 < 32768; r7++) {
            FindR7 finder = new FindR7(r7);
            finder.warmCache();
            finder.r0 = 4;
            finder.r1 = 1;
            finder.fn6027();
            int answer = finder.r0;
            System.out.println(r7 + " -> " + answer);
            if (answer == 6) {
                System.out.println("Found answer: r7=" + r7);
                return;
            }
        }
        throw new IllegalStateException("Answer not found");
    }


}
