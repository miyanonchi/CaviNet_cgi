#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $page_id = $query->param("PageID");
my $lang_id = $query->param("LanguageID");
my $name = $query->param("name");

if ($page_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "PageID"});
    exit;
}

if ($lang_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

if ($name eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "name"});
    exit;
}

# コンマが入るとCaviNet,Cavigator側で問題が出るので、全角に変換する
$name =~ s/,/，/;

# DBに接続
my $dbh = &super::connectDB;
my $sth;

my $record = &super::getValue($dbh, "TPage", [], {PageID => $page_id, LanguageID => $lang_id});

if ($record eq undef) { # レコードが無いとき
    $sth = $dbh->prepare("insert into TPage values ('$lang_id', '$page_id', '$name')");
    $sth->execute();
} else { # レコードがあるとき
	$sth = $dbh->prepare("update TPage set Name = '$name' where LanguageID = '$lang_id' and PageID = '$page_id'");
	$sth->execute();
}

&super::printCGIHeader("C200", "Success!");

exit;
