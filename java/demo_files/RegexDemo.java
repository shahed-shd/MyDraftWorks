import java.io.PrintStream;
import java.util.Arrays;
import java.util.function.Predicate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class RegexDemo {
    public static final PrintStream printStream = System.out;

    public static void main(final String[] args) {
        printStream.println("Hello Java");

        final String regex = "a*b";
        final String str1 = "aaB";
        final String str2 = "aabkaxbkkambb";

        // ---------- Pattern ----------

        assert "\\QaaB\\E".equals(Pattern.quote(str1));
        assert Pattern.matches("(?i)" + regex, str1); // (?i) to indicate case insensitive
        assert !Pattern.matches(regex, str2);

        Pattern p = Pattern.compile(regex, Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE);

        assert regex.equals(p.pattern());
        assert p.flags() == (Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE);

        Predicate<String> pred = p.asPredicate();
        assert pred.test(str1); // true, pattern is found in a given input string.
        assert pred.test(str2); // true, pattern is found in a given input string.

        Predicate<String> matchPred = p.asMatchPredicate();
        assert matchPred.test(str1); // true, this pattern matches the given input string.
        assert !matchPred.test(str2); // false, this pattern doesn't match the given input string.

        String[] splitted = p.split(str2);
        assert splitted.length == 3;
        assert Arrays.equals(splitted, new String[] { "", "kax", "kkam" });

        Stream<String> stream = p.splitAsStream(str2);
        assert stream.count() == splitted.length;

        // ---------- Matcher ----------

        Matcher m = p.matcher(str1);
        assert m.matches();
        assert m.pattern() == p;

        m.reset(str2); // Change the input string. Matcher's pattern also can be changed via
                       // usePattern(Pattern newPattern) method
        assert m.regionStart() == 0;
        assert m.regionEnd() == str2.length();
        // region can be modified via region() method

        assert m.lookingAt();

        assert "RAkaxRAkkamRARA".equals(m.replaceAll("RA"));
        m.reset();

        assert "RFkaxbkkambb".equals(m.replaceFirst("RF"));
        m.reset();

        StringBuffer sb1 = new StringBuffer();
        StringBuffer sb2 = new StringBuffer();

        printStream.println("str: " + str2);
        printStream.println("regex: " + regex);

        while (m.find()) {
            printStream.printf("%ngroup: %s, start: %d, end: %d%n", m.group(), m.start(), m.end());

            m.appendReplacement(sb1, "REP");
            printStream.println("appendReplacement: " + sb1.toString());

            m.appendTail(sb2);
            printStream.println("appendTrail: " + sb2.toString());
        }

        assert m.hitEnd();
    }
}