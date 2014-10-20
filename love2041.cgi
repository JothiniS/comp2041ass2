#!/usr/bin/perl -w

# written by Jothini Sivananthan September 2014
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/LOVE2041/

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
warningsToBrowser(1);

# print start of HTML ASAP to assist debugging if there is an error in the script
print page_header();

# some globals used through the script
$debug = 1;
$students_dir = "./students";

print browse_screen();
print page_trailer();
exit 0;	

sub browse_screen {
	my $n = param('n') || 0;
	my @students = glob("$students_dir/*");
	$n = min(max($n, 0), $#students);
	param('n', $n + 1);
	my $student_to_show  = $students[$n];
	my $profile_filename = "$student_to_show/profile.txt";
#     my $style = get_style();  
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
	$profile = join '', <$p>;
         $profile=~s/name:\n.*\n//gi;
         $profile=~s/email:\n.*\n//gi;
         $profile=~s/usercourses:\n.*\n//gi;
	$profile=~s/courses:\n.*\n//gi;
         $profile=~s/password:\n.*\n//gi;

	 my $profile_pic = "$student_to_show/profile.jpg";
	 print "<img src=$profile_pic>";
#print "Content-type: text/html\n\n";
#	 print "<img src =/ass2/heart-of-love.jpg>";
#print "</body>;
#print "</html>;
# print textfield('field_name','starting value',50,80);	
 #  print password_field('secret','starting value',50,80);
   print filefield('uploaded_file','starting value',50,80);	    	
	return p,
		start_form, "\n",
		pre($profile),"\n",
		hidden('n', $n + 1),"\n",
		submit('Next student'),"\n",
		end_form, "\n",
		p, "\n";
}
print header,
	start_html('A simple example'),
	h2('The Ulitmate Love Match'),
	end_html;

#
# HTML placed at bottom of every screen
#
sub page_header {
	return header,
   		start_html("-title"=>"The Ultimate Love Match", -bgcolor=>"#FEDCBA",
-background=>"heart-of-love.jpg");
	
 		center(h2(i("The Ultimate Love Match")));
}

#
# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	$html .= end_html;
	return $html;
}
 
