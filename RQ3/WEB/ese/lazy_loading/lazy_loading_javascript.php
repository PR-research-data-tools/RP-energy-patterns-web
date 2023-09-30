<?php

// Select correct variant
$loading = "eager";
if (isset($_GET["loading"])) {
    $loading = $_GET[ "loading" ];
}

switch($loading) {
    case "lazy":
        $jsCode = "
        document.addEventListener('DOMContentLoaded', pageInit, false);
        document.addEventListener('scroll', recurrentLoad, false);
        window.addEventListener('resize', recurrentLoad, false);
        ";
        break;
    case "eager":
        $jsCode = "
        document.addEventListener('DOMContentLoaded', loadEverything, false);
        ";
        break;
    default:
        $jsCode = "";
}

?>

<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lazy Loading - javaScript</title>
    <link rel="stylesheet" href="lazy_loading.css">
    
    <script src="lazy_loading_javascript.js"></script>
    
    <script type="text/javascript">
        <?php
            echo $jsCode;
        ?>
    </script>
    

</head>

<body>
    <h1>Lazy Loading - javaScript</h1>
    <p>Image Credits: Lorem Picsum (<a href="https://picsum.photos" target="_blank">https://picsum.photos</a>)</p>
    <hr />
    <div id="image-gallery">
    </div>
    <div class="clearfix"></div>
</body>
</html>