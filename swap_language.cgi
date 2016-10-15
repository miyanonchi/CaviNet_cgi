#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $lang_id = $query->param("LanguageID");

if ($lang_id eq "") {
	&super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

my @id = split(",", $lang_id);

if (scalar(@id) != 2) {
	&super::printCGIHeader("E111", "It needs two parameters that separated by comma.", {Param => "LanguageID"});
	exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# ファイルの入ったパスを取得する
my @rec1 = &super::getValue($dbh, "Language", [], {LanguageID => $id[0]});

if (scalar(@rec1) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my @rec2 = &super::getValue($dbh, "Language", [], {LanguageID => $id[1]});

if (scalar(@rec2) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my $n0 = (split(",", $rec1[0]))[1];
my $n1 = (split(",", $rec2[0]))[1];

$sth = $dbh->prepare("update Language set Name = '$n1' where LanguageID = '$id[0]'");
$sth->execute();

$sth = $dbh->prepare("update Language set Name = '$n0' where LanguageID = '$id[1]'");
$sth->execute();

&super::printCGIHeader("C200", "Success!");

exit;
