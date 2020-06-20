<?php

function test_input($data)
{
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

echo var_dump($_REQUEST);
echo "<br>";
echo var_dump($_GET);
echo "<br>";
echo var_dump($_POST);
echo "<br>";

foreach($_REQUEST as $k => $val) {
    echo "$k : $val <br>";
}

?>