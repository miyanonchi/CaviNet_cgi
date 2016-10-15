#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $loc_id = $query->param("LocationID");
my $seq_to = $query->param("Sequence");
my $name = $query->param("name");

if ($loc_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "LocationID"});
    exit;
}

if ($name eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "name"});
    exit;
}

# コンマが入るとCaviNet,Cavigator側で問題が出るので、全角に変換する
$name =~ s/,/，/;

# DBに接続
my $dbh = &super::connectDB;
my $sth;

my $record = &super::getValue($dbh, "Location", [], {LocationID => $loc_id});

if ($record eq undef) { # レコードが無いとき
	if ($seq_to eq "") {
		&super::printCGIHeader("E101", "No param.", {Param => "Sequence"});
		exit;
	}

    $sth = $dbh->prepare("insert into Location values ('$loc_id', '$name', $seq_to)");
    $sth->execute();
} else { # レコードがあるとき
	if ($seq_to eq "") { # シーケンスが無いとき(Nameを更新)
		$sth = $dbh->prepare("update Location set Name = '$name' where LocationID = '$loc_id'");
		$sth->execute();
	} else { # シーケンスがあるとき(順番入れ替える+Nameを更新)
		my $seq_from = (split(",", $record))[2];

		# 順番ずらす
		if ($seq_to < $seq_from) {
			$sth = $dbh->prepare("update Location set Sequence = Sequence + 1 where Sequence between $seq_to and $seq_from");
			$sth->execute();
		} elsif ($seq_from < $seq_to) {
			$sth = $dbh->prepare("update Location set Sequence = Sequence - 1 where Sequence between $seq_from and $seq_to");
			$sth->execute();
		}

		# 情報の更新
		$sth = $dbh->prepare("update Location set Name = '$name', Sequence = $seq_to where LocationID = '$loc_id'");
		$sth->execute();
	}
}

&super::printCGIHeader("C200", "Success!");

exit;
