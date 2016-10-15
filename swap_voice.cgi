#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use File::Copy;
use CGI::Carp qw(fatalsToBrowser);
require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
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

my @lan = split(",", $lan_id);

if (scalar(@lan) != 2) {
    &super::printCGIHeader("E111", "It needs two parameters separated by comma.", {Param => "LanguageID"});
    exit;
}

my @loc =split(",", $loc_id);

if (scalar(@loc) != 2) {
    &super::printCGIHeader("E111", "It needs two parameters separated by comma.", {Param => "LocationID"});
    exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# ファイルの入ったパスを取得する
my @rec0 = &super::getValue($dbh, "Voice", [], {LanguageID => $lan[0],LocationID => $loc[0]});

if (scalar(@rec0) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my @rec1 = &super::getValue($dbh, "Voice", [], {LanguageID => $lan[1],LocationID => $loc[1]});
if (scalar(@rec1) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my ($d0, $p0) = (split(",", $rec0[0]))[2, 3];
my ($d1, $p1) = (split(",", $rec1[0]))[2, 3];

$sth = $dbh->prepare("update Voice set Date = '$d1' where LanguageID = '$lan[0]' and LocationID = '$loc[0]'");
$sth->execute();

$sth = $dbh->prepare("update Voice set Date = '$d0' where LanguageID = '$lan[1]' and LocationID = '$loc[1]'");
$sth->execute();

move($p0, "hoge");
move($p1, $p0);
move("hoge", $p1);

&super::printCGIHeader("C200", "Success!");

exit;
