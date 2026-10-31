<?php
/**
 * GURO PSP — auto-deploy from GitHub (public repo artemguro/guropsp-site).
 * Runs from cron every 10 minutes. If site/VERSION on GitHub differs from the deployed one,
 * downloads the repo zip and copies the site/ folder into the web root. Never deletes files,
 * never touches /tg/ (bot webhook) or anything outside the web root.
 * Then pings IndexNow (Bing, Yandex) with URLs that are new in sitemap.xml.
 */
declare(strict_types=1);

const REPO    = 'artemguro/guropsp-site';
const BRANCH  = 'main';
const WEBROOT = '/home/igamzpbl/guropsp.com';
const DATA    = __DIR__ . '/data';
const INDEXNOW_KEY = '5f3c9e2a7b1d4c8e9a6f0b2d3c4e5f61';
const ALLOWED = ['html', 'css', 'js', 'xml', 'txt', 'png', 'jpg', 'jpeg', 'svg', 'ico', 'webmanifest', 'webp', 'htaccess'];

@mkdir(DATA, 0750, true);
$lock = fopen(DATA . '/lock', 'c');
if (!$lock || !flock($lock, LOCK_EX | LOCK_NB)) exit(0);

function logm(string $m): void {
    file_put_contents(DATA . '/deploy.log', gmdate('Y-m-d H:i:s') . " $m\n", FILE_APPEND);
}

function http_get(string $url, ?string $saveTo = null): ?string {
    $ch = curl_init($url);
    $opts = [CURLOPT_FOLLOWLOCATION => true, CURLOPT_TIMEOUT => 120, CURLOPT_CONNECTTIMEOUT => 15,
             CURLOPT_USERAGENT => 'guropsp-deploy', CURLOPT_FAILONERROR => true];
    $fh = null;
    if ($saveTo) { $fh = fopen($saveTo, 'w'); $opts[CURLOPT_FILE] = $fh; } else { $opts[CURLOPT_RETURNTRANSFER] = true; }
    curl_setopt_array($ch, $opts);
    $res = curl_exec($ch);
    $err = curl_error($ch);
    curl_close($ch);
    if ($fh) fclose($fh);
    if ($res === false) { logm("GET failed $url: $err"); return null; }
    return $saveTo ? 'ok' : (string)$res;
}

function sitemap_urls(string $xml): array {
    preg_match_all('#<loc>([^<]+)</loc>#', $xml, $m);
    return $m[1] ?? [];
}

$force = in_array('--force', $argv ?? [], true);
$remote = http_get('https://raw.githubusercontent.com/' . REPO . '/' . BRANCH . '/site/VERSION?t=' . time());
if ($remote === null) exit(1);
$remote = trim($remote);
$local = is_file(DATA . '/version') ? trim((string)file_get_contents(DATA . '/version')) : '';
if (!$force && ($remote === '' || $remote === $local)) exit(0);

$zipPath = DATA . '/repo.zip';
if (http_get('https://codeload.github.com/' . REPO . '/zip/refs/heads/' . BRANCH, $zipPath) === null) exit(1);

$zip = new ZipArchive();
if ($zip->open($zipPath) !== true) { logm('zip open failed'); exit(1); }

$oldSitemap = is_file(WEBROOT . '/sitemap.xml') ? sitemap_urls((string)file_get_contents(WEBROOT . '/sitemap.xml')) : [];
$written = 0; $skipped = 0;
for ($i = 0; $i < $zip->numFiles; $i++) {
    $name = $zip->getNameIndex($i);
    // entries look like "guropsp-site-main/site/blog/x/index.html"
    if (!preg_match('#^[^/]+/site/(.+)$#', $name, $m)) continue;
    $rel = $m[1];
    if (substr($rel, -1) === '/') continue;                       // directory entry
    if (strpos($rel, '..') !== false || $rel[0] === '/') { $skipped++; continue; }
    if (preg_match('#^(tg|cgi-bin|\.well-known)/#', $rel)) { $skipped++; continue; }
    $base = basename($rel);
    $ext = $base === '.htaccess' ? 'htaccess' : strtolower(pathinfo($base, PATHINFO_EXTENSION));
    if (!in_array($ext, ALLOWED, true) || $base === 'VERSION') { $skipped++; continue; }
    $dest = WEBROOT . '/' . $rel;
    @mkdir(dirname($dest), 0755, true);
    $data = $zip->getFromIndex($i);
    if ($data === false) { $skipped++; continue; }
    if (is_file($dest) && md5_file($dest) === md5($data)) continue;
    file_put_contents($dest . '.tmp', $data);
    rename($dest . '.tmp', $dest);
    $written++;
}
$zip->close();
@unlink($zipPath);
file_put_contents(DATA . '/version', $remote);
logm("deployed $remote: $written files updated, $skipped skipped");

// IndexNow: new URLs from the sitemap (all URLs on the very first run are skipped to avoid spam)
$newSitemap = is_file(WEBROOT . '/sitemap.xml') ? sitemap_urls((string)file_get_contents(WEBROOT . '/sitemap.xml')) : [];
$fresh = $oldSitemap ? array_values(array_diff($newSitemap, $oldSitemap)) : [];
if ($fresh) {
    $body = json_encode(['host' => 'guropsp.com', 'key' => INDEXNOW_KEY, 'keyLocation' => 'https://guropsp.com/' . INDEXNOW_KEY . '.txt', 'urlList' => $fresh]);
    foreach (['https://api.indexnow.org/indexnow', 'https://yandex.com/indexnow'] as $ep) {
        $ch = curl_init($ep);
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 20,
                                CURLOPT_HTTPHEADER => ['Content-Type: application/json; charset=utf-8']]);
        curl_exec($ch);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        logm("indexnow $ep -> HTTP $code for " . count($fresh) . ' urls');
    }
}
