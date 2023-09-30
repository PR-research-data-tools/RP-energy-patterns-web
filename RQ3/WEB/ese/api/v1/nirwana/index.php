<?php

require_once("../../../middleware/trait.API.php");

class Handler {
    use API;
    
    protected $sleepSeconds = 2;
    
    public function handle() {
        sleep($this->sleepSeconds);
				//echo("HOOORAY");
        $this->abort_with_error(503, "Sorry for any inconvenience");
    }
}

// Run handler
$handler = new Handler();
$handler->handle();


?>