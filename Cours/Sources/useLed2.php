<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="styleM1.css" />
    <title> Une page de test </title>
</head>

<body>
  <h1> Gestion de LED </h1>

  <form action="useLed2.php" method="post">

    <p>
      <label for="freq">Fréquence</label>
      <input type="number" name="freq" id="freq" />
   </p>
     <button type="submit" id="clignote" name="clignote">Clignoter</button>
     <button type="submit" id="eteindre" name="eteindre">Eteindre</button>

  </form>

<?php
  if (isset($_POST["clignote"]) || isset($_POST["eteind"])){
	   if (isset($_POST["clignote"])){
        $frequence = $_POST["freq"];
	      $command = escapeshellcmd("python3 clientLed2.py clignote $frequence");
        $output = shell_exec($command);
	   }
     else {
          $command = escapeshellcmd("python3 clientLed2.py eteind");
     }

     echo "<p>";
	   echo "commande envoyee :";
	   echo $command;

     $output = shell_exec($command);
     echo $output;
     echo "</p>";
  }
?>
</body>
</html>
