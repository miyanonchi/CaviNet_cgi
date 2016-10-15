#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use File::Copy;

require 'dbaccess.cgi';

&super::printHeader;

my $buf;

my $query = new CGI;

# CGIのパラメータを取得
my $tbl;
my @cols;
my %where;

foreach my $key ($query->param) {
    if ($key eq "tbl") {
        $tbl = $query->param($key);
    } elsif ($key eq "cols") {
        @cols = $query->param($key);
    } else {
        $where{$key} = $query->param($key);
    }
}

# DBに接続
my $dbh = &super::connectDB;

# ファイルの入ったパスを取得する
my @res = &super::getValue($dbh, $tbl, \@cols, \%where);

foreach my $l (@res) {
	if ($l ne "") {
		$buf = $buf . $l . "\n";
	}
}

&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

print $buf;

exit;
