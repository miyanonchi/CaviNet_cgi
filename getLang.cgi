#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

require 'dbaccess.cgi';

&super::printHeader;

my $buf;

my $dbh = &super::connectDB;

my @langs = &getLanguage($dbh);

foreach my $l (@langs) {
    $buf = $buf . $l."\n";
}

&super::disconnectDB($dbh);

&super::printCGIHeader("C200", "Success!");

print $buf;

exit;

sub getLanguage {
    my $dbh = shift(@_);
    my @langs;

    # SQLをセットして実行
    my $sth = $dbh->prepare("select LanguageID, Name from Language");
    $sth->execute;
    
    # 結果を取り出して配列にプッシュ
    while (my ($i, $n) = $sth->fetchrow_array) {
        push(@langs, $i.", ".$n);
    }

    $sth->finish;

    return @langs;
}
