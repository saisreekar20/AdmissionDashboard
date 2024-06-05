<?php
// Database connection parameters
$servername = "sql12.freesqldatabase.com";
$username = "sql12711951";
$password = "XGnGcadYwE";
$database = "sql12711951";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "";


?>
