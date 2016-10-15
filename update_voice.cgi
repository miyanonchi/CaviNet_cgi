#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use File::Copy;
use File::Path;
use File::Basename;

require 'dbaccess.cgi';

#my @exts = ("mp3", "wav", "aiff", "ogg");

&super::printHeader;

$CGI::POST_MAX = 1024 * 1024 * 50;

my $query = new CGI;

# CGIのパラメータを取得
my $lan_id = $query->param("LanguageID");
my $lct_id = $query->param("LocationID");

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

if ($ext != "mp3") {
	&super::printCGIHeader("E109", "Invalid extension.", {Extenstion => $ext});
	exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

my $path = &super::getValue($dbh, "Voice" ,[], {LanguageID => $lan_id, LocationID => $lct_id});

if ($path eq undef) { # レコードが無いとき
	#$path = "$super::cavi_dir/$lan_id/Voice/$lct_id.ogg";
        $path = "$super::cavi_dir/$lan_id/Voice/$lct_id.mp3";

	$sth = $dbh->prepare("insert into Voice values ('$lan_id', '$lct_id', '" . &super::datetime . "', '$path')"); 
	$sth->execute;
} else { # レコードがあるとき
    $path = (split(",", $path))[3];

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

if (!-d dirname($path)) {
    mkpath(dirname($path))
}

if (-d dirname($path)) {
    copy($file_handle, $path);

=pod # コメントアウト ここから
    my $st = 0;

	# ファイルをコピーして変換
	if ($ext eq "ogg") {
	    copy($file_handle, $path);
	} elsif ($ext eq "mp3") {
	    copy($file_handle, "/tmp/hoge");
	    $st = system("mpg321 /tmp/hoge -w - > /tmp/huga; oggenc /tmp/huga -q 6 -o $path");
	} else {
	    copy($file_handle, "/tmp/hoge");
	    $st = system("oggenc /tmp/hoge -q 6 -o $path");
	}

	if ($st != 0) {
		&super::printCGIHeader("E112", "Failed convert the file.");
		exit;
	}
=cut # ここまで

} else {
    &super::printCGIHeader("E107", "Can't make the path.", {Solution => "ディレクトリの権限を確認する"});
    exit;
}

$sth = $dbh->prepare("update Voice set Date = '" . &super::datetime . "', Path = '$path' where LanguageID = '" . $lan_id . "' and LocationID = '" . $lct_id . "'");
$sth->execute;

&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

exit;

sub StringGetFileName(){
    my ($string) = @_;
    return ($string =~ /([^\\\/:]+)$/) ? $1 : $string;
}
