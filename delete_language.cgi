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

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# ファイルの入ったパスを取得する
my @record = &super::getValue($dbh, "Language", [], {LanguageID => $lang_id});

if (scalar(@record) == 0) { # レコードが無い場合
    &super::printCGIHeader("E102", "No record.");
    exit;
}

$sth = $dbh->prepare("delete from Text where LanguageID = '$lang_id'");
$sth->execute();
$sth = $dbh->prepare("delete from Voice where LanguageID = '$lang_id'");
$sth->execute();

$sth = $dbh->prepare("delete from TPage where LanguageID = '$lang_id'");
$sth->execute();
$sth = $dbh->prepare("delete from TLocation where LanguageID = '$lang_id'");
$sth->execute();

$sth = $dbh->prepare("delete from Language where LanguageID = '$lang_id'");
$sth->execute();

&super::printCGIHeader("C200", "Success!");
exit;
