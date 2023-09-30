<?php

require_once("../../../middleware/trait.API.php");
require_once("../../../middleware/class.DBhandler.php");

class Handler {
    use API;
    
    protected $DB_TESTRUNS = 'ese_testruns';
    protected $DB_VARIANTS = 'ese_test_variants';
    protected $dbHandler;
    
    public function handle() {
        $this->restrict_http_method('GET,POST,PUT');
        
        $this->dbHandler = new DBhandler();
        
        // Check http method
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $result = $this->collectData();
            if ($result !== null) {
                if (isset($_GET['id'])) {
                    $response = $result[$_GET['id']];
                }
                else {
                    $response = $result;                    
                }
            }
            else {
                $this->abort_with_error(503, "Could not read from database");
            }
        }
        elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $json = file_get_contents('php://input');
            $data = json_decode($json, true);
            $result = $this->newTestrun($data);
            if (result !== false) {
                $response = $result;
            }
            else {
                $this->abort_with_error(503, "Could not write to database");
            }
        }
        elseif ($_SERVER['REQUEST_METHOD'] === 'PUT') {
            $json = file_get_contents('php://input');
            $data = json_decode($json, true);
            $result = $this->updateTestrun($data);
            if (result !== false) {
                $response = $result;
            }
            else {
                $this->abort_with_error(503, "Could not update database");
            }
        }
        
        // Return result
        $json = json_encode($response);
        header("Content-Type: application/json; charset=UTF-8");
        echo $json;
    }
    
    
    protected function newTestrun($data) {
        $requirements = array("id", "name");
        if ($this->verifyJsonContent($data, $requirements)) {
            $format = "REPLACE INTO %s (id, name, started) VALUES ('%s', '%s', now())";
            $q = sprintf($format,
                         $this->DB_TESTRUNS,
                         $data['id'],
                         $data['name']);
            return $this->dbHandler->query($q);
        }
        else {
            $this->abort_with_error(400, "Invalid message body");
        }
    }
    
    
    protected function updateTestrun($data) {
        $requirements = array("id", "action");
        if ($this->verifyJsonContent($data, $requirements)) {
            switch ($data["action"]) {
                case "run":
                    return $this->updateVariant($data);
                case "end":
                    return $this->endTestcase($data);
                default:
                    $this->abort_with_error(400, "Invalid message body");
            }
        }
        else {
            $this->abort_with_error(400, "Invalid message body");
        }
    }
    
    protected function updateVariant($data) {
        $requirements = array("variant", "name");
        if ($this->verifyJsonContent($data, $requirements)) {
            $format = "INSERT INTO %s (test_id, variant, name, counter, last_update) VALUES ('%s', %d, '%s', 1, now()) ON DUPLICATE KEY UPDATE counter = counter + 1, last_update = now()";
            $q = sprintf($format,
                         $this->DB_VARIANTS,
                         $data['id'],
                         $data['variant'],
                         $data['name']);
            return $this->dbHandler->query($q);
        }
        else {
            $this->abort_with_error(400, "Invalid message body");
        }
    }
    
    protected function endTestcase($data) {
        $format = "UPDATE %s SET ended = now() WHERE id = '%s'";
        $q = sprintf($format,
                     $this->DB_TESTRUNS,
                     $data['id']);
        return $this->dbHandler->query($q);
    }
    
    
    protected function collectData() {
        $format = "SELECT * FROM %s";
        
        // Fetch all testruns
        $q = sprintf($format, $this->DB_TESTRUNS);
        $result = $this->dbHandler->query($q);
        $testruns = $result->fetch_all(MYSQLI_ASSOC);
        
        // Fetch all test variants
        $q = sprintf($format, $this->DB_VARIANTS);
        $result = $this->dbHandler->query($q);
        $variants = $result->fetch_all(MYSQLI_ASSOC);
        
        // Now, combine them
        // Start with testruns
        $protocol = array();
        foreach ($testruns as $t) {
            $entry = array(
                'info' => $t,
                'variants' => []
            );
            $protocol[$t['id']] = $entry;
        }
        
        // Add variant info
        foreach ($variants as $v) {
            if (array_key_exists($v['test_id'], $protocol)) {
                $protocol[$v['test_id']]['variants'][] = $v;
            }
        }
        
        return $protocol;
    }
}

// Run handler
$handler = new Handler();
$handler->handle();


?>