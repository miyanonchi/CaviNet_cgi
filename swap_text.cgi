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
my $lan_id = $query->param("LanguageID");
my $page_id = $query->param("PageID");

if ($lan_id eq "") {
   &super::printCGIHeader("E101", "No param.", {Param => "Language"});
    exit;
}

if ($page_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "PageID"});
    exit;
}

my @lan = split(",", $lan_id);

if (scalar(@lan) != 2) {
    &super::printCGIHeader("E111", "It needs two parameters separated by comma.", {Param => "LanguageID"});
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
my @rec1 = &super::getValue($dbh, "Text", [], {LanguageID => $lan[0], PageID => $pag[0]});

if (scalar(@rec1) == 0) { # レコードが無い場合                                                                                                                                                   
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my @rec2 = &super::getValue($dbh, "Text", [], {LanguageID => $lan[1], PageID => $pag[1]});

if (scalar(@rec2) == 0) { # レコードが無い場合                                                                                                                                                   
    &super::printCGIHeader("E102", "No record.");
    exit;
}

my ($d0, $p0) = (split(",", $rec1[0]))[2, 3];
my ($d1, $p1) = (split(",", $rec2[0]))[2, 3];

$sth = $dbh->prepare("update Text set Date = '$d1', Path = '$p0' where LanguageID = '$lan[0]' and PageID = '$pag[0]'");
$sth->execute();

$sth = $dbh->prepare("update Text set Date = '$d0', Path = '$p1' where LanguageID = '$lan[1]' and PageID = '$pag[1]'");
$sth->execute();

move($p0, "hoge");
move($p1, $p0);
move("hoge", $p1);

&super::printCGIHeader("C200", "Success!");

exit;
