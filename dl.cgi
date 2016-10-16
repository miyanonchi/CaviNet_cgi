#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

require "dbaccess.cgi";

my $query = CGI->new();
my $filepath = $query->param("file");

if (!$filepath) {
	&super::printHeader();
    &super::printCGIHeader("E101", "No param.", {Param => "file"});
    exit;
}

$filepath = "/var/www/" . $filepath;

if ($filepath =~ /\.\./ || $filepath =~ /~/) {
	&super::printHeader();
	&super::printCGIHeader("E113", "The Filepath contains invalid character.", {Character => "'..' or '~'"});
   exit;
}

if (!-e $filepath) {
	&super::printHeader();
	&super::printCGIHeader("E114", "File not found.");
	exit;
}

my $size = -s $filepath;
my $filename = &StringGetFileName($filepath);

# とりあえずOctet-Streamで送っとく
print "Content-Type: application/octet-stream\n";
print "Content-Length: $size\n";
print "Content-Disposition: attachment; filename=\"$filename\"\n";
print "\n";

open(FILE, "<$filepath");

# 忘れてはいけない・・・
binmode(FILE);

while(<FILE>) {
	print $_;
}
close(FILE);

exit;

sub StringGetFileName(){
    my ($string) = @_;
    return ($string =~ /([^\\\/:]+)$/) ? $1 : $string;
}
