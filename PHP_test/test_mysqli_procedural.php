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
        # ---------- To show errors ----------
        ini_set('display_errors', 1);
        ini_set('display_startup_errors', 1);
        error_reporting(E_ALL);

        # ---------- Open a Connection to MySQL ----------
        $servername = 'localhost';
        $username = 'root';
        $password = 'abcd1234';

        $conn = mysqli_connect($servername, $username, $password);

        if(!$conn) {
            die("Connection failed: " . mysqli_connect_error());
        }

        echo "Connected successfully. <br>";

        # ---------- Creating a database ----------
        $dbname = "myDBSQLiProc";
        $sql = "CREATE DATABASE IF NOT EXISTS $dbname";

        if(mysqli_query($conn, $sql)) {
            echo "Database created successfully. <br>";
        }
        else {
            echo "Error creating database: " . mysqli_error($conn) . "<br>";
        }

        $sql = "USE $dbname";
        mysqli_query($conn, $sql);
        echo "Using database $dbname <br>";

        # ---------- Creating table ----------
        $sql = "CREATE TABLE IF NOT EXISTS myguests (
            id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(30) NOT NULL,
            lastname VARCHAR(30) NOT NULL,
            email VARCHAR(50),
            reg_date TIMESTAMP)";

        if(mysqli_query($conn, $sql)) {
            echo "Table MyGuests created successfully. <br>";
        }
        else {
            echo "Error creating table: " . mysqli_error($conn), "<br>";
        }

        # ---------- Inserting record ----------
        $sql = "INSERT INTO myguests (firstname, lastname, email)
            VALUES ('John', 'Doe', 'john@example.com')";

        if (mysqli_query($conn, $sql)) {
            $last_id = mysqli_insert_id($conn);
            echo "New record created successfully. Last inserted id: " . $last_id . "<br>";
        } else {
            echo "Error: " . $sql . "<br>" . mysqli_error($conn) . "<br>";
        }

        # ---------- Inserting multiple records ----------
        $sql = "INSERT INTO myguests (firstname, lastname, email)
            VALUES ('John', 'Doe', 'john@example.com');";
        $sql .= "INSERT INTO myguests (firstname, lastname, email)
            VALUES ('Mary', 'Moe', 'mary@example.com');";
        $sql .= "INSERT INTO myguests (firstname, lastname, email)
            VALUES ('Julie', 'Dooley', 'julie@example.com')";

        if(mysqli_multi_query($conn, $sql)) {
            echo "New records created successfully. <br>";
            while(mysqli_more_results($conn)) {   // Flush multi_queries.
                echo "FLUSHING... <br>";
                mysqli_next_result($conn);
            }
        }
        else {
            echo "Error: " . $sql . "<br>" . mysqli_error($conn) . "<br>";
        }

        # ---------- Select data ----------
        $sql = "SELECT id, firstname, lastname FROM myguests";
        $result = mysqli_query($conn, $sql);

        if(!$result) {
            trigger_error(mysqli_error($conn));
        }

        if(mysqli_num_rows($result) > 0) {
            echo "<table> <tr> <th>ID</th> <th>Name</th> </tr>";
            while($row = mysqli_fetch_assoc($result)) {
                echo "<tr> <td>" . $row['id'] . "</td> <td>" . $row['firstname'] . " " . $row['lastname'] . "</td> </tr>";
            }
            echo "</table>";
        }
        else {
            echo '0 results <br>';
        }

        # Close the Connection
        mysqli_close($conn);
        echo "Connection closed. <br>";
    ?>

     <!-- ---------- Short tag ---------- -->
    <!-- <p> In p tag, using short tag: <?=$a?></p> -->
</body>
</html>