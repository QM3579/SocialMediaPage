#!/usr/bin/perl -wT

use strict;
use CGI;

 my $q = CGI->new;
          


my $username=$q->param('username');
my $realname=$q->param('name');
my $password=$q->param('password');
##my @friends;

my $file = '../data/members.csv' ;
open(INFO, "<$file");
my @info = <INFO>;
close(INFO);
print "Content-type: text/html\n\n";
print "<body bgcolor=\"#99CCFF\"><center>";

#print "<p> $info[0] $username $realname $password </p> ";
my @usernames;
my @temp;
my $i;
my $line;

if ($username eq '' || $realname eq '' || $password eq ''){

print "<p> One of the fields is empty. Please try again. <br> </p>";
print "<a href=\"http://cs.mcgill.ca/~xwang200/member.html\">Return to Registration</a>";

exit 0;
}

for ($i=0;$i<=$#info;$i++){

        $line = $info[$i];
	@temp = split( '\s', $line);
	$usernames[$i]=$temp[1];
}

#print "<p> @usernames </p>";

for ($i=0;$i<=$#usernames;$i++)
{
	
 if ($usernames[$i] eq $username){
	#print "Content-type: text/html\n\n";
	print "<P>ERROR, INVALID USERNAME <BR> </P>";
	print "<a href=\"http://cs.mcgill.ca/~xwang200/Welcome.html\">Return to main page</a>";

	
	exit;
 }
}


open (APPEND, ">>../data/members.csv");
print APPEND "$realname $username $password \n";
close (APPEND);

#print "Content-type: text/html\n\n";
print " <P> Registration successful. Please return to the main menu to login. <BR> <BR> </P> ";
print "<a href=\"http://cs.mcgill.ca/~xwang200/Welcome.html\">Return to main page</a> ";
print "</center></body>";