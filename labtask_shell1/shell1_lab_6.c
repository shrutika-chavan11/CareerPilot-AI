#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    // Check if environment variable COUNT exists
    char *count = getenv("COUNT");

    // First execution (COUNT not present)
    if (count == NULL)
    {
        printf("First execution\n");

        // Create environment variable COUNT=1
        // Environment survives exec()
        setenv("COUNT", "1", 1);

        // Replace current process with a fresh copy
        // Program starts again from main()
        execl("./selfexec", "selfexec", NULL);

        // Executes only if exec() fails
        perror("execl");
        exit(1);
    }

    // Second execution:
    // getenv("COUNT") != NULL
    // if block skipped, so no more exec()
    printf("Second execution\n");

    return 0;
}
