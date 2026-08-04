#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
    printf("calling 1st fork\n");
    int pid = fork();
    
    if(pid == 0) {
       printf("child1 : child of 1st fork\n");
       int p = fork();
       if(p == 0) {
          printf("child of 2nd fork\n");
       }
       else {
           wait(NULL);
          printf("child1 : waiting\n");
          
      }
    } 
    else {
         wait(NULL);
        printf("PARENT : waiting\n"); 
       
        
    }
  
    return 0;
 }
