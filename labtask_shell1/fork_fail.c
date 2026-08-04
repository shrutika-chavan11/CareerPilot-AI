#include <stdio.h>
#include <unistd.h>

int main()
{
    while (1)
    {
        pid_t pid = fork();

        if (pid == -1)
        {
            perror("fork");
            break;
        }
    }

    return 0;
}
