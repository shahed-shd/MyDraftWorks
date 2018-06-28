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
        # To show errors.
        ini_set('display_errors', 1);
        ini_set('display_startup_errors', 1);
        error_reporting(E_ALL);

        # Just an echo.
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
        /*
        $a = 1234;
        $b = "It's a string type value";
        $c = true;
        $arr = ['aa', 'bb', 'cc'];
        $arr_assoc = [0=>"abc", 'd'=>'def', 'g'=>'ghi'];

        echo "<br> $a <br> $b <br> $c <br>";
        var_dump($arr);
        echo "<br>";
        var_dump($arr_assoc);
        echo "<br>";

        $s = "abcdefghij";
        printf("[%'*-15.7s]", $s);   // print 7 characters of the string, occupying 15 character space, padding wiht *, left justified.
        echo "<br>";
        */

        # ---------- str_getcsv() example ----------
        /*$csv_file_path = '/home/shahed/ShdHomeData/MyDraftWorks/TestFolder/contacts.csv';
        $csv = explode("\n", file_get_contents($csv_file_path));

        foreach($csv as $csvline) {
            $s =  str_getcsv($csvline);
            echo "$s[0] : $s[34] <br>";
        }*/

        # ---------- Error handling ----------
        /*
        function customError($errno, $errstr) {
            echo "<b>Error:</b> [$errno] $errstr";
        }

        set_error_handler("customError");

        $abc = 5;
        echo "<br>" . $abc . "<br>";

        if($abc > 1) {
            trigger_error("Error goes on !");
        }
        */

        # ---------- MySQL ----------
        /*
        $conn = new mysqli("localhost", "root", "abcd1234");

        var_dump($conn->connect_error);

        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        echo "Connected successfully";
        */

    ?>

     <!-- ---------- Short tag ---------- -->
    <!-- <p> In p tag, using short tag: <?=$a?></p> -->
</body>
</html>