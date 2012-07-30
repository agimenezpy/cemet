<?php
/**
 * Map Action Plugin:   Map Component.
 * 
 * @author     Alberto G. <albergimenez@gmail.com>
 */
 
if(!defined('DOKU_INC')) die();
if(!defined('DOKU_PLUGIN')) define('DOKU_PLUGIN',DOKU_INC.'lib/plugins/');
require_once(DOKU_PLUGIN.'action.php');
 
class action_plugin_gMapViewer_maps extends DokuWiki_Action_Plugin {
 
  /**
   * return some info
   */
  function getInfo(){
    return array(
		 'author' => 'Alberto G.',
		 'email'  => 'albergimenez@gmail.com',
		 'date'   => '2009-05-13',
		 'name'   => 'Maps (action plugin component)',
		 'desc'   => 'Maps action functions.',
		 'url'    => 'http://www.guiadigital.com.py',
		 );
  }
 
  /**
   * Register its handlers with the DokuWiki's event controller
   */
  function register(&$controller) {
    $controller->register_hook('TPL_METAHEADER_OUTPUT', 'BEFORE',  $this, '_hookjs');
  }
 
  /**
   * Hook js script into page headers.
   *
   * @author Alberto G. <albergimenez@gmail.com>
   */
  function _hookjs(&$event, $param) {
    global $conf;
    global $ID;
    if ($ID == "modelo:brams") {
        $apikey = $this->getConf('gmapapikey');
        $theme = $this->getConf('theme');
        $event->data["script"][] = array ("type" => "text/javascript",
                    "charset" => "utf-8",
                    "_data" => "",
                    "src" => "http://maps.google.com/maps?file=api&v=2.x&key=$apikey&hl=es"
                    );
        $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => "/static/jquery/js/jquery-1.6.2.min.js"
            );
        $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => "/static/jquery/js/jquery-ui-1.8.16.custom.min.js"
            );
        $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => "/static/jquery/js/jquery.ui.datepicker-es.js"
            );
        $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => "/static/jquery/js/selectToUISlider.min.js"
            );
        $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => "/static/gMapViewer/main.js"
        );
        $event->data["link"][] = array (
          "type" => "text/css",
          "rel" => "stylesheet",
          "href" => "/static/gMapViewer/CTransparency.css"
        );
        $event->data["link"][] = array (
          "type" => "text/css",
          "rel" => "stylesheet",
          "href" => "/static/jquery/css/$theme/jquery-ui-1.8.16.custom.css"
        );
        $event->data["link"][] = array (
          "type" => "text/css",
          "rel" => "stylesheet",
          "href" => "/static/jquery/css/ui.slider.extras.css"
        );
    }
  }
}
