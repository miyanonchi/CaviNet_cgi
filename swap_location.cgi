#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $loc_id = $query->param("LocationID");

if ($loc_id eq "") {
	&super::printCGIHeader("E101", "No param.", {Param => "LocationID"});
    exit;
}

my @id = split(",", $loc_id);

if (scalar(@id) != 2) {
	&super::printCGIHeader("E111", "It needs two parameters separated by comma.", {Param => "LocationID"});
	exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# ファイルの入ったパスを取得する
my @rec0 = &super::getValue($dbh, "Location", [], {LocationID => $id[0]});

if (scalar(@rec0) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my @rec1 = &super::getValue($dbh, "Location", [], {LocationID => $id[1]});

if (scalar(@rec1) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my $seq0 = (split(",", $rec0[0]))[2];
my $seq1 = (split(",", $rec1[0]))[2];

$sth = $dbh->prepare("update Location set Sequence = 65535 where LocationID = '$id[1]'");
$sth->execute();

$sth = $dbh->prepare("update Location set Sequence = $seq1 where LocationID = '$id[0]'");
$sth->execute();

$sth = $dbh->prepare("update Location set Sequence = $seq0 where LocationID = '$id[1]'");
$sth->execute();

&super::printCGIHeader("C200", "Success!");

exit;
