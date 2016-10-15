#!/usr/bin/perl

use strict;
use warnings;
use File::Copy;
use File::Basename;
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
    &super::printCGIHeader("E101", "No param.", {Param => "PageID"});
    exit;
}

my @pic = split(",", $pic_id);

if (scalar(@pic) != 2) {
	&super::printCGIHeader("E111", "It needs two parameters separated by comma.", {Param => "PictureID"});
	exit;
}

my @pag = split(",", $page_id);

if (scalar(@pag) != 2) {
	&super::printCGIHeader("E111", "It needs two parameters separated by comma.", {Param => "PageID"});
	exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# ファイルの入ったパスを取得する
my @rec1 = &super::getValue($dbh, "Picture", [], {PictureID => $pic[0], PageID => $pag[0]});

if (scalar(@rec1) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my @rec2 = &super::getValue($dbh, "Picture", [], {PictureID => $pic[1], PageID => $pag[1]});

if (scalar(@rec2) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my ($d0, $p0) = (split(",", $rec1[0]))[2, 3];
my ($d1, $p1) = (split(",", $rec2[0]))[2, 3];

# 拡張子の交換
my $e0;
my $e1;

if ($p0 =~ /.+\.(.+)/) {
	$e0 = $1;
}

if ($p1 =~ /.+\.(.+)/) {
	$e1 = $1;
}

move($p0, "hoge");

if ($p0 =~ /(.+)\..+/) {
	$p0 = "$1.$e1";
}

move($p1, $p0);

if ($p1 =~ /(.+)\..+/) {
	$p1 = "$1.$e0";
}

move("hoge", $p1);

$sth = $dbh->prepare("update Picture set Date = '$d1', Path = '$p0' where PictureID = '$pic[0]' and PageID = '$pag[0]'");
$sth->execute();

$sth = $dbh->prepare("update Picture set Date = '$d0', Path = '$p1' where PictureID = '$pic[1]' and PageID = '$pag[1]'");
$sth->execute();

&super::printCGIHeader("C200", "Success!");

exit;
