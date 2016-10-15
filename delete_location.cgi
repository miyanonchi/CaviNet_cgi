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

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# ファイルの入ったパスを取得する
my @record = &super::getValue($dbh, "Location", [], {LocationID => $loc_id});

if (scalar(@record) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my $seq = (split(",", $record[0]))[2];

# 行を削除
$sth = $dbh->prepare("delete from Voice where LocationID = '$loc_id'");
$sth->execute();

$sth = $dbh->prepare("delete from TLocation where LocationID = '$loc_id'");
$sth->execute();

$sth = $dbh->prepare("delete from Location where LocationID = '$loc_id'");
$sth->execute();

# 順番をずらす
$sth = $dbh->prepare("update Location set Sequence = Sequence - 1 where $seq < Sequence");
$sth->execute();

&super::printCGIHeader("C200", "Success!");

exit;
