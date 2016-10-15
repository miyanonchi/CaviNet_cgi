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

$sth = $dbh->prepare("select Page.PageID, TPage.Name from Page, TPage where TPage.LanguageID = '$lng' and Page.PageID = TPage.PageID order by Sequence");
$sth->execute();

my @text = &super::getValue($dbh, "Text", [], {LanguageID => $lng});
my @pic  = &super::getValue($dbh, "Picture", [], {});

# ページID 場所名 テキストファイル名 画像ファイル名
# オーダがnの2乗。パフォーマンス・・・
while (my @p = $sth->fetchrow_array()) {
	$buf = $buf . "$p[0],$p[1]";

	my $i;
	for ($i = 0; $i < $sth->rows; ++$i) {
		my ($id, $path) = (split(",", $text[$i]))[0,3];

		if ($p[0] eq $id) {
			$buf = $buf . "," . StringGetFileName($path);
			last;
		}
	}

	if ($i == $sth->rows) {
		$buf = $buf . ",";
	}

	my @picts = ();
	for ($i = 0; $i < $sth->rows; ++$i) {
		my ($id, $path) = (split(",", $pic[$i]))[1,3];

		if ($p[0] eq $id) {
			push(@picts, StringGetFileName($path));
		}
	}

	if (scalar(@picts) == 0) {
		$buf = $buf . ",";
	} else {
		$buf = $buf . "," . join(",", @picts);
	}

	$buf = $buf . "\n";
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
