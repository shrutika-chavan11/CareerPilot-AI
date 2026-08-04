#include <stdio.h>
#include <unistd.h>

int main()
{
    printf("Program Started\n");

    execl("./sl15", NULL);

    printf("This will never print\n");

    return 0;
}
