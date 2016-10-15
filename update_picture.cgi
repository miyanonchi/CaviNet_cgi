#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Copy;
use File::Path;
use File::Basename;

require 'dbaccess.cgi';

my @exts = ("jpg", "jpeg", "png");

&super::printHeader;

$CGI::POST_MAX = 1024 * 1024 *100;

my $query = new CGI;

# CGIのパラメータを取得
my $page_id = $query->param("PageID");
my $pict_id = $query->param("PictureID");

if ($page_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "PageID"});
    exit;
}

if ($pict_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "PictureID"});
    exit;
}

my $file_handle = $query->upload("data");
if (!$file_handle && $query->cgi_error) {
    &super::printCGIHeader("E103", "Can't receive the data.");
    exit;
}

my $filename = &StringGetFileName($file_handle);

# 拡張子を取得する
my $ext = "";
if ($filename =~ /.+\.(.+)/) {
    $ext = lc $1;
} else {
    &super::printCGIHeader("E108", "The file has no extension.");
    exit;
}

my $flag = 1;
for my $e (@exts) {
	if ($ext eq $e) {
		$flag = 0;
		last;
	}
}

if ($flag) {
	&super::printCGIHeader("E109", "Invalid extension.", {Extenstion => $ext});
	exit;
}

if ($ext eq "jpeg") {
	$ext = "jpg";
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# 結果は0個か1個のはず。たぶん。
my $path = &super::getValue($dbh, "Picture", [], {PictureID => $pict_id, PageID => $page_id});

if ($path eq undef) { # レコードが無いとき
    # パスを作る
	$path = "$super::cavi_dir/Picture/$page_id" . "_" . "$pict_id.$ext";  

    # レコードを作る
    $sth = $dbh->prepare("insert into Picture values ('$pict_id', '$page_id', '" . &super::datetime . "', '$path')"); 
    $sth->execute;
} else { # レコードがあるとき
    $path = (split(/,/, $path))[3];

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

$path =~ s/(.+\.).+/$1$ext/g;

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

$sth = $dbh->prepare("update Picture set Date = '" . &super::datetime . "', Path = '$path' where PictureID = '$pict_id' and PageID = '$page_id'");
$sth->execute;

&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

exit;

sub StringGetFileName {
    my ($string) = @_;
    return ($string =~ /([^\\\/:]+)$/) ? $1 : $string;
}
