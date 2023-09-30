<?php

// Select correct variant
if (isset($_GET["dynamic"])) {
    $jsCode = "goForIt(6, 1000, true);";
    $title = "exponential";
}
else {
    $jsCode = "goForIt(30, 3000, false);";
    $title = "constant";
}

?>

<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ESE - Dynamic Retry Delay</title>    
    <script src="dynamic_retry_delay.js" type="module"></script>
	<script type="text/javascript">
		function startNudging() {
			<?php echo($jsCode); ?>
			
		}
		
		document.addEventListener('DOMContentLoaded', startNudging, false);
	</script>
	<style>
		.log-entry {
			white-space: pre-wrap;
		}
	</style>
</head>

<body>
    <h1>Dynamic Retry Delay – <?=$title?></h1>
    <hr />
    <div id="logger">
    </div>
</body>
</html>
