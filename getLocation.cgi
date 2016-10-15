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

my $que = new CGI;

# DBに接続
my $dbh = &super::connectDB;
my $sth;

# CGIに渡されたテーブル名を取得してチェック
my $lng = $que->param('lang');

if (!$lng) {
    &super::printCGIHeader("E101", "No param.", {Param => "LanguageID"});
    exit;
}

$sth = $dbh->prepare("select Location.LocationID, TLocation.Name, Voice.Path from Location, TLocation, Voice where TLocation.LanguageID = '$lng' and Voice.LanguageID = '$lng' and Location.LocationID = Voice.LocationID and Location.LocationID = TLocation.LocationID order by Sequence");
$sth->execute();

# ロケーションID 現地の名前 音声ファイル名
while (my @p = $sth->fetchrow_array()) {
	$buf = $buf . $p[0] . "," . $p[1] . "," . StringGetFileName($p[2]) . "\n";
}

# DBと接続を切る
&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");
print $buf;

exit;

sub StringGetFileName(){
    my ($string) = @_;
    return ($string =~ /([^\\\/:]+)$/) ? $1 : $string;
}
