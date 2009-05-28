<?php
/*
  This is an example of how a local.php coul look like.
  Simply copy the options you want to change from dokuwiki.php
  to this file and change them
 */


$conf['start']       = 'Inicio';
$conf['title']          = 'Centro Meteorol&oacute;gico';
$conf['lang']           = 'es';
$conf['savedir']        = '/home/agimenez/Desktop/cemetwiki/dokuwiki/data/';
$conf['recent']         = 0;
$conf['breadcrumbs']    = 0;
$conf['youarehere']     = 1;
$conf['dformat']        = '%d/%m/%Y %H:%M';
$conf['useacl']         = 1;
$conf['disableactions'] = 'register,backlinks,index,recent,revisions,subscribe,subscribens,source';
$conf['updatecheck']    = 0;
$conf['send404']        = true;
$conf['template']    = 'cemet';
$conf['userewrite']  = 0;
$conf['htmlok']      = 1;

/* The following options are usefull, if you use a MySQL
 * database as autentication backend. Have a look into
 * mysql.conf.php too and adjust the options to match
 * your database installation.
 */
//$conf['authtype']   = 'mysql';
//require_once ("mysql.conf.php");
$conf['authtype'] = 'pgsql';
$conf['defaultgroup']= 'cms';
$conf['passcrypt']   = 'ssha';
$conf['superuser']   = 'admin';    //The admin can be user or @group or comma separated list user1,@group1,user2
$conf['manager']     = '@manager';    //The manager can be user or @group or comma separated list user1,@group1,user2
$conf['auth']['pgsql']['server'] = 'localhost';
$conf['auth']['pgsql']['user'] = 'gisadm';
$conf['auth']['pgsql']['password'] = 'ge0spatial';
$conf['auth']['pgsql']['database'] = 'cemet';
$conf['auth']['pgsql']['forwardClearPass'] = 1;

$conf['auth']['pgsql']['checkPass'] = "SELECT password AS pass
                                         FROM auth_user_groups AS ug
                                         JOIN auth_user AS u ON u.id = ug.user_id
                                         JOIN auth_group AS g ON g.id = ug.group_id
                                        WHERE u.username = '%{user}'
                                          AND g.name = '%{dgroup}'
                                          AND substring(password from E'\\\\$([a-z0-9]+)$') = ENCODE(DIGEST(substring(password from E'\\\\$([a-z0-9]+)\\\\$') || '%{pass}', substring(password from E'^([a-z0-9]+)\\\\$')), 'hex')";

$conf['auth']['pgsql']['getUserInfo'] = "SELECT password AS pass,
                                                translate(regexp_replace(first_name || ' ' || last_name, '([αινσϊ])', E'&\\\\1acute;'), 'αινσϊ', 'aeiou') AS name,
                                                email AS mail
                                          FROM auth_user
                                          WHERE username = '%{user}'";
                                          
$conf['auth']['pgsql']['getGroups'] = "SELECT g.name AS group
                                         FROM auth_group g, auth_user u, auth_user_groups ug
                                        WHERE u.id = ug.user_id
                                          AND g.id = ug.group_id
                                          AND u.username = '%{user}'";