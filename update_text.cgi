#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Copy;
use File::Path;
use File::Basename;

require 'dbaccess.cgi';

&super::printHeader;

$CGI::POST_MAX = 1024 * 1024 *10;

my $query = new CGI;

# CGIのパラメータを取得
my $page_id = $query->param("PageID");
my $lang_id = $query->param("LanguageID");

if ($page_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "PageID"});
    exit;
}

if ($lang_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

my $file_handle = $query->upload("data");
if (!$file_handle || $query->cgi_error) {
    &super::printCGIHeader("E103", "Can't receive the data.");
    exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;
my $path;

# ファイルの入ったパスを取得する
my $record = &super::getValue($dbh, "Text", [], {LanguageID => $lang_id, PageID => $page_id});

if ($record eq undef) { # レコードが無いとき
    $path = "$super::cavi_dir/$lang_id/Text/$page_id.txt";
    $sth = $dbh->prepare("insert into Text values ('$page_id', '$lang_id', '" . &super::datetime. "', '$path')");
    $sth->execute;   

} else { # レコードがあるとき
    $path = (split(',', $record))[3];

    if ($path eq undef) {
        &super::printCGIHeader("E106", "Filepath was not set.", {Solution => "項目を削除して、やり直す"});
        exit;
    }

    if (-e $path) {
        # 削除する
        unlink($path);

        if (-e $path) {
            &super::printCGIHeader("E104", "Can't delete file.", {Solution => "ディレクトリまたはファイルの権限を確認する"});
            exit;
        }
    } else {
        # エラー処理
        &super::printCGIHeader("E105", "The file path recorded, but the file was not exist.", {Solution => "項目を削除して、やり直す"});
        exit;
    }
}

my $filename = &StringGetFileName($file_handle);
if (!-d dirname($path)) {
    mkpath(dirname($path))
}

if (-d dirname($path)) {
    # ファイルをコピー
    copy($file_handle, $path);
} else {
    &super::printCGIHeader("E107", "Can't make the path.", {Solution => "ディレクトリの権限を確認する"});
    exit;
}

$sth = $dbh->prepare("update Text set Date = '" . &super::datetime . "' where PageID = '" .$page_id.  "' and LanguageID = '" .$lang_id . "'");
$sth->execute;

&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

exit;

sub StringGetFileName(){
    my ($string) = @_;
    return ($string =~ /([^\\\/:]+)$/) ? $1 : $string;
}
