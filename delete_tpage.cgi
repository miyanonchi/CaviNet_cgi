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

if ($page_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "PageID"});
    exit;
}

if ($lang_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

my $record = &super::getValue($dbh, "TPage", [], {PageID => $page_id, LanguageID => $lang_id});

if ($record eq undef) { # レコードが無いとき
	&super::printCGIHeader("E102", "No record.");
	exit;
} else { # レコードがあるとき
	$sth = $dbh->prepare("delete from TPage where LanguageID = '$lang_id' and PageID = '$page_id'");
	$sth->execute();
}

&super::printCGIHeader("C200", "Success!");

exit;
