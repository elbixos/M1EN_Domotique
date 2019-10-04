<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="styleM1.css" />
    <title> Une page de test </title>
</head>

<body>
  <h1> Gestion de LED </h1>

  <form action="useLed.php" method="post">

    <p>
      <label for="freq">Fréquence</label>
      <input type="number" name="freq" id="freq" />
   </p>
     <button type="submit" id="submit" name="submit">Clignoter</button>

  </form>

  <?php
  if (isset($_POST["submit"])){
      $frequence = $_POST["freq"];
      $command = escapeshellcmd("python3 testArg.py $frequence");
      $output = shell_exec($command);

      echo "<p>";
      echo $output;
      echo "</p>";
  }
  ?>
</body>
</html>
