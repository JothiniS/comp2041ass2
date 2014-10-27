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
print header();
print start_html("-title"=>"The Ultimate Love Match", -bgcolor=>"#FEDCBA", -background=>"heart-of-love.jpg");
print center(h2(i("The Ultimate Love Match")));

# some globals used through the script
$debug = 1;
$students_dir = "./students";
print browse_screen();
if (defined param('foo')) {
 print hidden('foo');
   print browse_screen();
} else {
  print login_screen();
 print  authenticate_password();
   
}
print page_trailer();
exit 0;	
#s[0-9]\s+[A-Z]+[0-9]+
#(+s[0-9]\s+[A-Z]+[0-9]+) // brackets help store captureinto variable $1
sub browse_screen {
	my $n = param('n') || 0;
	my @students = glob("$students_dir/*");
	$n = min(max($n, 0), $#students);
	param('n', $n + 1);
	my $student_to_show  = $students[$n];
	my $profile_filename = "$student_to_show/profile.txt";
#     my $style = get_style();  
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
	my $profile = join '', <$p>;
        # close $p;
         $profile=~s/name:\n.*\n//gi;
         $profile=~s/email:\n.*\n//gi;
         $profile=~s/usercourses:\n.*\n//gi;
        $profile=~s/couses:[0-9]{4}\s+[A-Z]+[0-9]+//g;
         $profile=~s/courses:\s+((([0-9]+\s+S[12]\s+[A-Z]+[0-9]+\s+)+)+)//g;
         $profile=~s/courses:\s+((([0-9]+\s+X[12]\s+[A-Z]+[0-9]+\s+)+)+)//g;
        $profile=~s/[0-9]{4}\s+S[12]\s+[A-Z]+[0-9]+//g;
        $profile=~s/[0-9]{4}\s+X[12]\s+[A-Z]+[0-9]+//g;
        
	$profile=~s/courses:\n.*\n//gi;
         $profile=~s/password:\n.*\n//gi;
	$person= $students[$n];
	$person=~m/.\/students\/(.*)/;
	print h1("$1");
 	 my $profile_pic = "$student_to_show/profile.jpg";
	 print "<img src=$profile_pic>";

#	$profile=<font size="3" color="black">;

   print filefield('uploaded_file','starting value',50,80);	    	
	return p,
		start_form, "\n",
		pre($profile),"\n",
		hidden('n', $n + 1),"\n",
		submit('Next student'),"\n",
		end_form, "\n",
		p, "\n";
}


#
# HTML placed at bottom of every screen
#


sub title_header {
	return start_html("-title"=>"The Ultimate Love Match"-bgcolor=>"#FEDCBA");
		center(h2(i("The Ultimate Love Match")));
}
# insecure: user may set this parameter directly
if (param('password_checked')) {
    if (param('student_number') && param('new_mark')) {
        mark_changed_screen();
    } else {
        change_mark_screen() 
    }
} elsif (defined param('login') && defined param('password')) {
    if (authenticate_password()) {
        param('password_checked', 1);
        change_mark_screen();
    } else {
        wrong_password_screen();
    }
} else {
    login_screen();
}

exit 0;

sub login_screen {
    print start_form,
        'Enter login: ', textfield('login'), "<br>\n",
        ' Enter password: ', password_field('password'),, "<br>\n",
        submit('Login'),
        #hidden('Login'),
        end_form,
        end_html;
}

sub wrong_password_screen {
    print "Login or password incorrect.\n", p;
    login_screen();
}


sub authenticate_password {
    my $login = param('login');
    my $password = param('password');
    print $password;
    $password_file = "./students/$login/profile.txt";
    print $password_file;
    if (!open F, "<$password_file") {
		print "Unknown username!\n";
	
	} else {
		while($correct_password=<F>){
			
		chomp $correct_password;
		if($correct_password=~m/password:/ ){
		       $correct_password = <F>;
		       chomp $correct_password;
		       print $correct_password;
		       $correct_password =~ s/^\s+//g;
		if ($password eq $correct_password) {
			
			print "You are authenticated.\n";
		#	param('student',$login);
			browse_screen();
			param('foo', 'foo');
			print hidden('foo');
			param('password_checked',$correct_password);
			print hidden('password_checked');
			
		} else {
			print "Incorrect password!\n";
			#wrong_password_screen();
		}
		}
	}
	}
    
    #./students/username/profile.txt
    #open <F>, ./students/username/profile.txt or die;
   return $login && $password && $login eq "andrewt" && $password eq "secret";
}

sub change_mark_screen {
    print start_form,
        'Enter 2041 student number: ', textfield('student_number'), "<br>\n",
        'Enter new mark: ', textfield('new_mark'), "<br>\n",
        submit('Change mark'),
        hidden('password_checked'),
        end_form,
        end_html;
}

sub mark_changed_screen {
    my $student_number = param('student_number');
    my $new_mark = param('new_mark');
    print  "Mark for $student_number set to $new_mark\n", p;
    change_mark_screen();
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
 
