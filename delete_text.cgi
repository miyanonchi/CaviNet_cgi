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

my $query = new CGI;

# CGIのパラメータを取得
my $page_id = $query->param("PageID");
my $lan_id = $query->param("LanguageID");

if ($page_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "PageID"});
    exit;
}

if ($lan_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;
my $path;

# ファイルの入ったパスを取得する
my @record = &super::getValue($dbh, "Text", [], {LanguageID => $lan_id, PageID => $page_id});

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
                &super::printCGIHeader("E104", "Can`t delete File.");
                exit;
            } else {
                $sth = $dbh->prepare("delete from Text where LanguageID = '$lan_id' and PageID = '$page_id'");
                $sth->execute;
            }
        } else {
            # エラー処理
            &super::printCGIHeader("E105", "The file path recorded, but the file was not exist.",
                                   {PageID => $page_id, LanguageID => $lan_id});
            exit;
        }
    }
}

&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

exit;
