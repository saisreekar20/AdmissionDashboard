<?php
session_start();
include("connection.php");

if(isset($_POST['submit'])){
    $username = $_POST['username'];
    $password = $_POST['password'];
    $role = $_POST['role'];

    $sql = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    $result = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    $count = mysqli_num_rows($result);

    if($count == 1){
        if($row['role'] == $role){
            if($role == 'admin'){
                echo '<script>
                        window.location.href="admin_dashboard.php";
                      </script>';
                exit();
            } elseif($role == 'user'){
                echo '<script>
                        window.location.href="user_dashboard.php";
                      </script>';
                exit();
            }
        } else {
            echo '<script>
                    window.location.href="index.php";
                    alert("Login failed. Invalid role.");
                  </script>';
        }
    } else {
        echo '<script>
                window.location.href="index.php";
                alert("Login failed. Invalid username or password");
              </script>';
    }
    
}
?>
