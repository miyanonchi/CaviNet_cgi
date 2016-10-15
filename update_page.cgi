#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

&super::printHeader;

my $query = new CGI;
my $page_id = $query->param("PageID");
my $seq_to = $query->param("Sequence");
my $name = $query->param("name");

if ($page_id eq "") {
    &super::printCGIHeader("E101", "No param.", {Param => "PageID"});
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

my $record = &super::getValue($dbh, "Page", [], {PageID => $page_id});

if ($record eq undef) { # レコードが無いとき
	if ($seq_to eq "") {
		&super::printCGIHeader("E101", "No param.", {Param => "Sequence"});
		exit;
	}

    $sth = $dbh->prepare("insert into Page values ('$page_id', '$name', $seq_to)");
    $sth->execute();
} else { # レコードがあるとき
	if ($seq_to eq "") { # シーケンスが無いとき(Nameを更新)
		$sth = $dbh->prepare("update Page set Name = '$name' where PageID = '$page_id'");
		$sth->execute();
	} else { # シーケンスがあるとき(順番入れ替える+Nameを更新)
		my $seq_from = (split(",", $record))[2];

		# 順番ずらす
		if ($seq_to < $seq_from) {
			$sth = $dbh->prepare("update Page set Sequence = Sequence + 1 where Sequence between $seq_to and $seq_from");
			$sth->execute();
		} elsif ($seq_from < $seq_to) {
			$sth = $dbh->prepare("update Page set Sequence = Sequence - 1 where Sequence between $seq_from and $seq_to");
			$sth->execute();
		}

		$sth = $dbh->prepare("update Page set Name = '$name', Sequence = $seq_to where PageID = '$page_id'");
		$sth->execute();
	}
}

&super::printCGIHeader("C200", "Success!");

exit;
