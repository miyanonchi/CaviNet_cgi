#!/usr/bin/perl

use strict;
use warnings;

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

require 'dbaccess.cgi';

# HTTPヘッダの出力
&super::printHeader;

my $buf;
my $size = 0;

my $que = new CGI;

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# CGIに渡されたテーブル名を取得してチェック
my $lng = $que->param('lang');
my $date = $que->param('date') || '00000000000000';

if (!$lng) {
    &super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

$buf = $buf . "http\:\/\/$ENV{HTTP_HOST}$ENV{PATH_INFO}/cgi-bin/getLocation.cgi?lang=$lng\n";
$buf = $buf . "http\:\/\/$ENV{HTTP_HOST}$ENV{PATH_INFO}/cgi-bin/getPage.cgi?lang=$lng\n";

$sth = $dbh->prepare("select Path from Voice where LanguageID = '" . $lng . "' and '" . $date . "' <= Date");
$sth->execute();

while (my $p = $sth->fetchrow_array) {
	$size += -s $p;
    $p =~ s/\/var\/www/http\:\/\/$ENV{HTTP_HOST}$ENV{PATH_INFO}/g;
    $buf = $buf . $p . "\n";
}

$sth = $dbh->prepare("select Path from Text where LanguageID = '" . $lng . "' and '" . $date . "' <= Date");
$sth->execute();

while (my $p = $sth->fetchrow_array) {
	$size += -s $p;
    $p =~ s/\/var\/www/http\:\/\/$ENV{HTTP_HOST}$ENV{PATH_INFO}/g;
    $buf = $buf . $p . "\n";
}

$sth = $dbh->prepare("select Path from Picture where '" . $date . "' <= Date");
$sth->execute();

while (my $p = $sth->fetchrow_array) {
	$size += -s $p;
    $p =~ s/\/var\/www/http\:\/\/$ENV{HTTP_HOST}$ENV{PATH_INFO}/g;
    $buf = $buf . $p . "\n";
}

# DBと接続を切る
&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");
print $size . "\n";
print $buf;

exit;
