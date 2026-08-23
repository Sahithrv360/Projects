#include <stdio.h>
#include <unistd.h>

int main() {

    printf("=== Program vs Process ===\n\n");

    printf("This is a program currently being executed.\n");

    printf("\nProcess Information:\n");
    printf("Process ID  : %d\n", getpid());
    printf("Parent PID  : %d\n", getppid());

    return 0;
}