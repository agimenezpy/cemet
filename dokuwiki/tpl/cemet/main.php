<?php
/**
 * DokuWiki Cemet Template
 *
 * This is the template you need to change for the overall look
 * of DokuWiki.
 *
 * You should leave the doctype at the very top - It should
 * always be the very first line of a document.
 *
 * @link   http://dokuwiki.org/templates
 * @author Alberto Giménez E.
 */

// must be run from within DokuWiki
if (!defined('DOKU_INC')) die();

require_once(dirname(__FILE__).'/tpl_functions.php');
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php echo $conf['lang']?>"
 lang="<?php echo $conf['lang']?>" dir="<?php echo $lang['direction']?>">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>
    <?php tpl_pagetitle()?> | .::. <?php echo strip_tags($conf['title'])?> .::.
  </title>

  <?php tpl_metaheaders()?>

  <link rel="shortcut icon" href="<?php echo DOKU_TPL?>images/favicon.ico" />

  <?php /*old includehook*/ @include(dirname(__FILE__).'/meta.html')?>
</head>

<body>
<div class="header">
  <div class="logo">
    <h1><?php tpl_link(wl(),$conf['title'],'name="dokuwiki__top" id="dokuwiki__top" accesskey="h" title="[H]"')?></h1>
    <p>Facultad Politécnica</p>
  </div>

  <div id="user-tools"><?php
    if ($_SERVER['REMOTE_USER']) {
    ?>
    <strong> <?php tpl_userinfo(); ?></strong> <?php tpl_actionlink('profile'); ?>&nbsp;/&nbsp;
    <?php tpl_actionlink('login'); ?>
    <?php } ?>
  </div>
  <div id="menu" class="dokuwiki">
    <ul>
        <li><?php tpl_searchform() ?></li>
    </ul>
  </div>
</div>

<div class="bar dokuwiki">
  <?php if($conf['youarehere']){?>
  <div class="bar-left">
  <?php tpl_youarehere() ?>
  <?php }?>
  </div>
  <div class="bar-right">
        <?php tpl_button('admin')?>
        <?php tpl_button('edit') ?>
        <?php tpl_button('history') ?>
        <?php tpl_button('recent') ?>
  </div>
</div>

<?php html_msgarea() ?>
<?php flush()?>

  <?php /*old includehook*/ @include(dirname(__FILE__).'/pageheader.html')?>

  <div id="page" class="dokuwiki">
  <!--div id="header-pic"></div-->
  <table class="layout" cellspacing="0" cellpadding="0" border="0" width="100%">
  <tr><td id="left_panel">
    
    <div id="sidebar">
    <h1>Tabla de contenidos</h1>
    <?php tpl_toc() ?>
    <div class="clear"></div>
    <?php if(tpl_getConf('sidebar') == 'left') { ?>
      <?php if(!tpl_sidebar_hide()) { ?>
        <div class="left_sidebar">
          <?php tpl_sidebar('left') ?>
        </div>
      <?php } ?>
    <?php } ?>
    </div>
    </td>
    <td id="right_panel">
        <!-- Content -->
        <div id="content">
          <!-- wikipage start -->
          <?php tpl_content(false)?>
          <!-- wikipage stop -->
          <br class="clear" />
        </div>
    </td></tr>
    </table>
    <div style="clear:both; margin:0;"></div>
  </div>

  <div class="clearer">&nbsp;</div>

  <?php flush()?>

  <div class="dokuwiki">
    <div id="footer">
      <p><strong>&copy; 2008. Facultad Politécnica, U.N.A. Todos los derechos reservados. <br>Design by <a href="mailto:info@pol.una.py">Alberto G.</a></strong></p>
    </div>
  </div>
</div>

<div class="no"><?php /* provide DokuWiki housekeeping, required in all templates */ tpl_indexerWebBug()?></div>
</body>
</html>
