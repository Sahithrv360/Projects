#include <stdio.h>
#include <unistd.h>

int main() {

    pid_t pid;

    printf("Before fork()\n");

    pid = fork();

    if (pid < 0) {
        printf("Process creation failed.\n");
    }
    else if (pid == 0) {
        printf("This is the Child Process.\n");
        printf("Child PID: %d\n", getpid());
        printf("Parent PID: %d\n", getppid());
    }
    else {
        printf("This is the Parent Process.\n");
        printf("Parent PID: %d\n", getpid());
        printf("Child PID: %d\n", pid);
    }

    return 0;
}