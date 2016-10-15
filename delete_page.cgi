#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $page_id = $query->param("PageID");

if ($page_id eq "") {
	&super::printCGIHeader("E101", "No param.", {Param => "PageID"});
    exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# ファイルの入ったパスを取得する
my @record = &super::getValue($dbh, "Page", [], {PageID => $page_id});

if (scalar(@record) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my $seq = (split(",", $record[0]))[2];

$sth = $dbh->prepare("delete from Text where PageID = '$page_id'");
$sth->execute();
$sth = $dbh->prepare("delete from Picture where PageID = '$page_id'");
$sth->execute();
$sth = $dbh->prepare("delete from TPage where PageID = '$page_id'");
$sth->execute();

$sth = $dbh->prepare("delete from Page where PageID = '$page_id'");
$sth->execute();

# 順番をずらす
$sth = $dbh->prepare("update Page set Sequence = Sequence - 1 where $seq < Sequence");
$sth->execute();

&super::printCGIHeader("C200", "Success!");
exit;
