
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv){
	if(argc != 4){
	printf("\n		Incorrect number of input arguments");
	printf("\n       PROPER USAGE IS ./gps -o inputfilename outputfilename.py\n");
	}else{
	
	char syscommand[100];
    char inputfilename[50];
    strcpy(inputfilename, argv[2]);
	char outputfilename[50];
    strcpy(outputfilename, argv[3]);
	strcpy(syscommand,"python3 gps.py ");
	strcat(syscommand, inputfilename);
	strcat(syscommand, " ");
	strcat(syscommand, outputfilename);
	
	system(syscommand);
	return 0;}
}
