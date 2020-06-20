<!DOCTYPE html>
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

        try {
            $conn = new PDO("mysql:host=$servername", $username, $password);
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            echo 'Connected successfully <br>';
        }
        catch (PDOException $e) {
            echo 'Connection failed: ' . $e->getMessage();
        }

        # ---------- Creating a database ----------
        $dbname = 'myDBPDO';

        try {
            $sql = "CREATE DATABASE IF NOT EXISTS $dbname";
            // Use exec() because no results are returned.
            $conn->exec($sql);
            echo 'Database created successfully <br>';
        }
        catch (PDOException $e) {
            echo $sql . '<br>' . $e->getMessage() . '<br>';
        }

        $sql = "USE $dbname";
        echo  $conn->exec($sql);
        echo "Using database $dbname <br>";

        # ---------- Creating table ----------
        $sql = "CREATE TABLE IF NOT EXISTS myguests (
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(30) NOT NULL,
            lastname VARCHAR(30) NOT NULL,
            email VARCHAR(50),
            reg_date TIMESTAMP
        )";

        $conn->exec($sql);
        echo 'Table created successfully. <br>';

        # ---------- Inserting record ----------
        $sql = "INSERT INTO myguests (firstname, lastname, email)
            VALUES ('John', 'Doe', 'john@example.com')";

        $conn->exec($sql);

        $last_id = $conn->lastInsertId();
        echo 'New record inserted successfully. Last inserted id: ' . $last_id . '<br>';

        # ---------- Inserting multiple records ----------
        $conn->beginTransaction();

        $conn->exec("INSERT INTO myguests (firstname, lastname, email)
            VALUES ('John', 'Doe', 'john@example.com')");
        $conn->exec("INSERT INTO myguests (firstname, lastname, email)
            VALUES ('Mary', 'Moe', 'mary@example.com')");
        $conn->exec("INSERT INTO myguests (firstname, lastname, email)
            VALUES ('Julie', 'Dooley', 'julie@example.com')");

        $last_id = $conn->lastInsertId();
        $conn->commit();
        echo 'New records inserted successfully. Last inserted id: ' . $last_id . '<br>';

        # ---------- Prepared statements ----------
        $stmt = $conn->prepare("INSERT INTO myguests (firstname, lastname, email)
            VALUES (:firstname, :lastname, :email)");

        $stmt->bindParam(':firstname', $firstname);
        $stmt->bindParam(':lastname', $lastname);
        $stmt->bindParam(':email', $email);

        $firstname = "John";
        $lastname = "Doe";
        $email = "john@example.com";
        $stmt->execute();

        $firstname = "Mary";
        $lastname = "Moe";
        $email = "mary@example.com";
        $stmt->execute();

        $firstname = "Julie";
        $lastname = "Dooley";
        $email = "julie@example.com";
        $stmt->execute();

        $last_id = $conn->lastInsertId();
        echo 'New records inserted successfully. Last inserted id: ' . $last_id . '<br>';

        # ---------- Select data ----------
        $sql = "SELECT id, firstname, lastname FROM myguests";
        $result = $conn->query($sql);

        if($result->rowCount() > 0) {
            echo "<table> <tr> <th>ID</th> <th>Name</th> </tr>";
            while($row = $result->fetch(PDO::FETCH_ASSOC)) {
                echo "<tr> <td>" . $row['id'] . "</td> <td>" . $row['firstname'] . " " . $row['lastname'] . "</td> </tr>";
            }
            echo "</table>";
        }
        else {
            echo '0 results <br>';
        }

        # ---------- Delete data ----------
        /*
        $sql = "DELETE FROM myguests WHERE id = 3";
        $conn->exec($sql);
        echo "Record deleted successfully. <br>";
        */

        # ---------- Update data ----------
        /*
        $sql = "UPDATE myguests
            SET lastname = 'Dooley'
            WHERE id = 1";

        $conn->exec($sql);

        echo "Data updated successfully. <br>";
        */

        # Close the Connection
        $conn = null;
    ?>

     <!-- ---------- Short tag ---------- -->
    <!-- <p> In p tag, using short tag: <?=$a?></p> -->
</body>
</html>