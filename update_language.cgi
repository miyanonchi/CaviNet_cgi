#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $lang_id = $query->param("LanguageID");
my $name = $query->param("name");

if ($lang_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LnaguageID"});
    exit;
}

if ($name eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "name"});
    exit;
}

# DBに接続
my $dbh = &super::connectDB;
my $sth;

my $record = &super::getValue($dbh, "Language", [], {LanguageID => $lang_id});

if ($record eq undef) { # レコードが無いとき
    $sth = $dbh->prepare("insert into Language values ('$lang_id', '$name')");
    $sth->execute();
} else { # レコードがあるとき
    $sth = $dbh->prepare("update Language set Name = '" . $name . "' where LanguageID = '" . $lang_id . "'");
    $sth->execute();
}

&super::printCGIHeader("C200", "Success!");

exit;
