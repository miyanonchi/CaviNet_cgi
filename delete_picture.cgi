#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $pic_id = $query->param("PictureID");
my $page_id = $query->param("PageID");

if ($pic_id eq "") {
   &super::printCGIHeader("E101", "No param.", {Param => "PictureID"});
    exit;
}

if ($page_id eq "") {
	&super::printCGIHeader("E101", "Noparam.", {Param => "PageID"});
	exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;
my $path;
# ファイルの入ったパスを取得する
my @record = &super::getValue($dbh, "Picture", [], {PictureID => $pic_id, PageID => $page_id});

if (scalar(@record) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
} else {
    foreach my $r (@record) {
        $path = (split(/,/, $r))[3];

        if (-e $path) {
            # 削除する
            unlink($path);

            if (-e $path) {
                &super::printCGIHeader("E104", "Can`t delete file.");
                exit;
            } else {
				$sth = $dbh->prepare("delete from Picture where PictureID = '$pic_id' and PageID = '$page_id'");
                $sth->execute;
            }
        } else {
            # エラー処理
            &super::printCGIHeader("E104", "The file path recorded, but the file was not exist.");
            exit;
        }
    }
}

&super::printCGIHeader("C200", "Success!");
exit;
