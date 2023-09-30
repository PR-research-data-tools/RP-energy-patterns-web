<?php

require_once("../../../middleware/class.HTMLTemplate.php");

header("Content-Type: application/json; charset=UTF-8");

$htmlTemplate = new HTMLTemplate();
$json = $htmlTemplate->fetchData();

$offset = 0;
$length = count($json);

if (isset($_GET['offset']) && $_GET['offset'] > 0) {
    $offset = $_GET['offset'];
}
if (isset($_GET['length']) && $_GET['length'] > 0) {
    $length = $_GET['length'];
}
$json = array_slice($json, $offset, $length);

echo json_encode($json);

?>