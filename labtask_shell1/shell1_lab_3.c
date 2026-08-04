#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>

int main()
{
    // Close standard output (file descriptor 1)
    close(1);

    // Open a file
    // Since fd 1 is free, open() will assign fd = 1
    int fd = open("output.txt", O_CREAT | O_WRONLY | O_TRUNC, 0644);

    if (fd == -1)
    {
        perror("open");
        exit(1);
    }

    printf("Hello, this output is redirected to a file.\n");
    printf("Operating Systems Practical\n");

    return 0;
}
