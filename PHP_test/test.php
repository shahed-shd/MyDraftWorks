<DOCTYPE <!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Index Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- <link rel="stylesheet" type="text/css" media="screen" href="main.css" /> -->
    <!-- <script src="main.js"></script> -->
</head>
<body>
    <h3>It is a heading.</h3>
    <?php
        echo "I am awesome !";

        # ---------- Comments ----------

        // Double slash is used for inline comment.
        # The # symbol is also used for inline comment.

        /* Just block-comment
        to comment out several lines. */

        // Can also be used to leave out parts of a code line
        $x = 5 /* + 15 */ + 5;
        echo "<br> x: $x <br>";

        #  ---------- Variables ----------

        $a = 1234;
        $b = "It's a string type value";
        $c = true;
        $arr = ['aa', 'bb', 'cc'];
        $arr_assoc = [0=>abc, d=>def, g=>ghi];

        echo "<br> $a <br> $b <br> $c <br>";
        var_dump($arr);
        echo "<br>";
        var_dump($arr_assoc);
        echo "<br>";

        $s = "abcdefghij";
        printf("[%'*-15.7s]", $s);   // print 7 characters of the string, occupying 15 character space, padding wiht *, left justified.
        echo "<br>";

        # ---------- str_getcsv() example ----------
        /*$csv_file_path = '/home/shahed/ShdHomeData/MyDraftWorks/TestFolder/contacts.csv';
        $csv = explode("\n", file_get_contents($csv_file_path));

        foreach($csv as $csvline) {
            $s =  str_getcsv($csvline);
            echo "$s[0] : $s[34] <br>";
        }*/

        echo $_SERVER["SCRIPT_URI"];
    ?>

    <p> In p tag, using short tag: <?=$a?></p>
</body>
</html>