#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define memberfile "../data/members.csv"

char inputstring[200];
int Inputlength;

char user[200];		//the attempted login credentials
char pass[200];

char temp1[200];	//strings to collect garbage
char temp2[200];

char userpass[9000];	//attempted login credentials in one single line
char decodedUserpass[9000]; //decoded credentials

char line[99999];		//lines used by the file reader


FILE *fp;


int AccessAllowed = 0; //boolean : 0 will deny access, 1 will allow

void DisplayLoginSuccessful(); 
void DisplayLoginFailed();
void decode (char source[], char dest[]);
char hexToAscii(char h1, char h2);



int main()

{

	printf("Content-type: text/html\n\n");
	printf("<html><body bgcolor=\"#99CCFF\">");
	
	Inputlength = atoi(getenv("CONTENT_LENGTH")) +1; //extra one
	

	fgets(inputstring, Inputlength, stdin);	//we read from stdin

	//we parse the input string in the form "username password" to compare with our members.csv file

	sscanf(inputstring,"%[^=]=%[^&]&%[^=]=%s", temp1, user, temp2, pass);
	strcpy(userpass,""); //initialize to null
	strcat(userpass, user);
	strcat(userpass, " ");
	strcat(userpass, pass);

	//if password or username contains symbols such as $^#&$%*,
	//we will decode them

	decode(userpass, decodedUserpass);

	//End of parsing. Now the string decodeduserpass contains the attempted login info.

	
//printf("<body>"); 
//printf("<p>You tried: %s</p>", decodedUserpass); 
	

	//Reading from the .csv
	
	fp = fopen(memberfile, "r");
	if(fp == NULL)
	{
		printf("<p>File path error</p>");
		printf( "</body></HTML>");

		exit(0);
	}
	
	while (fgets(line, sizeof(line), fp) != NULL && !feof(fp))
	{
		char *Cgarbage;
		char *Cuser;
		char *Cpass;

		char Cuserpass[9000]; //exisiting username and password combination






		Cgarbage = strtok(line, " ");	//we don't want the real name
		Cuser = strtok(NULL, " "); //get the second  word
		Cpass = strtok(NULL, " ");  //get the third word


		strcpy(Cuserpass,""); //initialize to null

		strcat(Cuserpass, Cuser);
		strcat(Cuserpass, " ");
		strcat(Cuserpass, Cpass);

		//at this point, we know that Cuserpass contains a valid user/pass combination
		//we want to compare it to the attempted login credentials

	 
//printf("<p>Existing combinations: %s</p>", Cuserpass); 
//printf("<p>checking %s vs: %s</p>", userpass, Cuserpass); 
//printf("<p>length of %s: %d, length of %s: %d</p>", userpass, sizeof(userpass),Cuserpass ,sizeof(Cuserpass));
//printf("<p>compare result: %d</p>", strcmp(Cuserpass, userpass)); 	

		//we now compare
		if (strcmp(Cuserpass, decodedUserpass) == 0)
		{
			DisplayLoginSuccessful();
			exit(0)	;		

		}
						
	}
	//at this point, we know that the attempted login credentials do not match with any
	//of the registered users.



	DisplayLoginFailed();


}

void DisplayLoginSuccessful()
{

printf("<center><h2>Login Successful!</h2><br><br><br><br><br><br><a href=\"http://cs.mcgill.ca/~xwang200/cgi-bin/MyFacebookPage.py\">Proceed to feed page</a>");

printf( "</center></body></HTML>");
}

void DisplayLoginFailed()
{

printf("<center><h2>Login Failed!</h2><br><br><br><br><br><br><a href=\"http://cs.mcgill.ca/~xwang200/Welcome.html\">Return to main page</a>");

printf( "</center></body></HTML>");
}


void decode (char source[], char dest[])   
{
    int sIndex = 0;
    int dIndex = 0;
    int sLength = strlen(source);
    
    while (sIndex < sLength)
    {
        if(source[sIndex] != '%')
        {
            dest[dIndex] = source[sIndex];
            sIndex++;
            dIndex++;
        }
        else
        {
            //get the next two numbers, those will be the corresponding ascii values

			int ASCII = 0;

			char hex1 = source[sIndex+1];
			char hex2 = source[sIndex+2];

			char realChar = hexToAscii(hex1, hex2);
			//convert to integer


			//convert back to symbol according to ascii value
			dest[dIndex] = realChar;

			//update indices
			sIndex = sIndex + 3;
			dIndex ++;
        }
        
        //printf("%d\n", currentChar);
    }
    
    
}


char hexToAscii(char h1, char h2)
{
	char hexCode[5];
	char *end;

	hexCode[0] = '0';
	hexCode[1] = 'x';
	hexCode[2] = h1;
	hexCode[3] = h2;
	hexCode[4] = 0;

	return strtol(hexCode, &end, 16);
}