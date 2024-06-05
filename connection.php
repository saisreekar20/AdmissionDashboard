<?php
// Database connection parameters
$servername = "sql12.freesqldatabase.com";
$username = "sql12708926";
$password = "3p2AnmtVla";
$database = "sql12708926";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "";


?>
