<?php

/**
 * HTML template
 */

class HTMLTemplate {
    protected $dataFilePath = __DIR__ . "/image_list.json";
    protected $newSize = [1200, 800];
    protected $jsonData;
    protected $loadType;

    /**
     * Constructor
     */
    public function __construct($loadType = "eager") {
        $this->loadType = $loadType;
    }
    
    
    /**
     * Load JSON data
     */
    public function loadData($filename = null) {
        if (is_null($filename)) {
            $filename = $this->dataFilePath;
        }
        if (!file_exists($filename)) {
            exit("ERROR: Unable to open file ($filename)");
        }
        $jsonString = file_get_contents($filename);
        $this->jsonData = json_decode($jsonString, true);
        $this->resizeImages();
    }
    
    
    /**
     * Load and return JSON data
     */
    public function fetchData($filename = null) {
        $this->loadData($filename);
        return $this->jsonData;
    }
    
    
    /**
     * Resize all images to newSize
     */
    protected function resizeImages() {
        foreach($this->jsonData as $key => $payload) {
            $originalImageUrl = $payload['download_url'];
            $firstPart = explode("/", $originalImageUrl, -2);
            $newUrlParts = array_merge($firstPart, $this->newSize);
            $this->jsonData[$key]['download_url'] = implode("/", $newUrlParts);
        }
    }
    

}

?>