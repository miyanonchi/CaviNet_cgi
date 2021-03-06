#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

require 'dbaccess.cgi';

&super::printHeader;

my $buf;

# DBに接続
my $dbh = &super::connectDB;

my $que = new CGI;

# CGIに渡されたテーブル名を取得してチェック
my $tbl = $que->param('tbl');

my $sth = $dbh->prepare("select * from " . $tbl);
$sth->execute;

# フィールド名を出力
$buf = $buf . $sth->{NAME}[0];
for (my $i = 1; $i < $sth->{NUM_OF_FIELDS}; ++$i) {
    $buf = $buf . "," . $sth->{NAME}[$i];
}
$buf = $buf . "\n";

# トランザクションを終了
$sth->finish;

# DBと接続を切る
&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

print $buf;

exit;
