#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

require 'dbaccess.cgi';

&super::printHeader;

my $buf;
my $sth;

# DBに接続
my $dbh = &super::connectDB;

my @tbls = &super::getTableName($dbh);

foreach my $tbl (@tbls) {
	$sth = $dbh->prepare("select * from " . $tbl);
	$sth->execute;

	$buf = $buf . "---------- $tbl ----------\n";

	$buf = $buf . join(",", @{$sth->{NAME}}) ."\n";

	# データを出力
	while (my @r = $sth->fetchrow_array) {
    	$buf = $buf . $r[0];
    	for (my $i = 1; $i < $sth->{NUM_OF_FIELDS}; ++$i) {
        	$buf = $buf . ",".$r[$i];
    	}
    	$buf = $buf . "\n";
	}

	$buf = $buf . "\n";
}

# トランザクションを終了
$sth->finish;

# DBと接続を切る
&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

print $buf;

exit;
