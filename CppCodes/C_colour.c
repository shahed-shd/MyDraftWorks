#include <stdio.h>

int main()
{
	short properties[5] = {0, 1, 4, 5, 7};
	short foreground[8];
	short i, p, f;

	for(i = 0; i <= 7; i++) foreground[i] = i + 30;

	printf("\033[1;9;7;36;45;49m");
        printf("I hate you... \n\n");
	printf("\033[0m");

	for(f = 0; f < 8; f++) {
		for(p = 0; p < 5; p++) {
			printf("\033[%hd;%hd;%hdm", properties[p], foreground[f], 49);
			printf("I love you, Mita... Love you so much forever... EKTAI AMAR TUMI...\n\n");
			printf("\033[0m");
		}
	}
    printf("\n\n");
	printf("\033[1;32;45;41m");
    printf("\n                                           \n\twhile(1) {\n\t\tlife = Mita <3 Shahed;\n\t}         \n                                           \n");
	printf("\033[0m");

	return 0;
}
