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
my $lan_id = $query->param("LanguageID");
my $loc_id = $query->param("LocationID");

if ($lan_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

if ($loc_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LocationID"});
    exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;
my $path;

# ファイルの入ったパスを取得する
my @record = &super::getValue($dbh, "Voice", [], {LanguageID => $lan_id, LocationID => $loc_id});

if ($record[0] eq undef) { # レコードが無い場合
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
                $sth = $dbh->prepare("delete from Voice where LanguageID = '$lan_id' and LocationID = '$loc_id'");
                $sth->execute;
            }
        } else {
            # エラー処理
            &super::printCGIHeader("E104", "The file path recorded, but the file was not exist.");
            exit;
        }
    }
}

&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

exit;
