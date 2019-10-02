<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title> Une page de test </title>
</head>

<body>
  <form action="startForm2.php" method="post">
    <button type="submit" id="submit" name="submit">Allumer</button>
  </form>

  <?php
  if (isset($_POST["submit"])){
      $command = escapeshellcmd('python3 turnOn1s.py');
      $output = shell_exec($command);
  }
  ?>
</body>
</html>
