#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $loc_id = $query->param("LocID");
my $lang_id = $query->param("LanguageID");

if ($loc_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LocID"});
    exit;
}

if ($lang_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

my $record = &super::getValue($dbh, "TLocation", [], {LocationID => $loc_id, LanguageID => $lang_id});

if ($record eq undef) { # レコードが無いとき
	&super::printCGIHeader("E102", "No record.");
	exit;
} else { # レコードがあるとき
	$sth = $dbh->prepare("delete from TLocation where LanguageID = '$lang_id' and LocationID = '$loc_id'");
	$sth->execute();
}

&super::printCGIHeader("C200", "Success!");

exit;
