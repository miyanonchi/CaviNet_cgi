#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

package super;

# DB接続に必要な各種情報
my $dbname = 'CaviNet';
my $server = 'localhost:3306';
my $user   = 'user';
my $pass   = 'cavinet.kut';

# グローバル変数
our $cavi_dir = '/var/www/CaviNet';

sub printHeader {
    # ヘッダ情報を出力
    print "Status: 200 OK!\n";
    print "Content-Type: text/plain;charset=utf-8;\n";
    print "\n";
}

sub printCGIHeader {
    my ($code, $msg, $hdr) = @_;

    print "Code: $code\n";
    print "Message: $msg\n";

    foreach my $key (keys %$hdr) {
        print "$key: " . %$hdr->{$key} . "\n";
    }

    print "\n";
}

sub datetime {
    my ($sec,$min,$hour,$mday,$mon,$year,undef,undef,undef) = localtime(time);
    $year += 1900;
    $mon += 1;

    return sprintf("%04d", $year).sprintf("%02d", $mon).sprintf("%02d", $mday)
      .sprintf("%02d", $hour).sprintf("%02d", $min).sprintf("%02d", $sec);
}

sub connectDB {
    my $dbh = DBI->connect('DBI:mysql:'.$dbname.':'.$server, $user, $pass)
	or die "Can not connect to database: ".DBI->errstr;

    return $dbh;
}

sub disconnectDB {
    my $dbh = shift(@_);

    $dbh->disconnect;
}

sub getTableName {
    my $dbh = shift(@_);
    my @tbls;

    # SQLをセットして実行
    my $sth = $dbh->prepare("show tables");
    $sth->execute;
    
    # 結果を取り出して配列にプッシュ
    while (my $t = $sth->fetchrow_array) {
        push(@tbls, $t);
    }

    $sth->finish;

    return @tbls;
}

sub getValue {
    # $dbh,$tblはスカラー
    # $colsは配列のリファレンス
    # $whereは連想配列のリファレンス
    my ($dbh, $tbl, $cols, $where) = @_;
    my @w = ();
    my $sql = "select ";

    if (scalar(@$cols) != 0) {
        $sql = $sql . join(",", @$cols);
    } else {
        $sql = $sql . "*";
    }

    $sql = $sql . " from " . $tbl;

    if (scalar(keys(%$where)) != 0) {
        foreach my $key (keys(%$where)) {
            if ($where->{$key} ne '') {
                push(@w, "$key = '$where->{$key}'");
            }
        }

        if (scalar(@w) != 0) {
            $sql = $sql . " where " . join(" and ", @w);
        }
	}

	if ($tbl eq "Page" || $tbl eq "Location") {
		$sql = $sql . " order by Sequence";
	}

    my $sth = $dbh->prepare($sql);
    $sth->execute;

    @w = ();

    # 結果を取り出して配列にプッシュ
	if ($sth->rows == 0) {
		return undef;
	}

    while (my @t = $sth->fetchrow_array) {
        push(@w, join(",", @t));
    }

    $sth->finish;

    if (@w == 1) {
        return $w[0];
    } else {
        return @w;
    }
}

1;
