#include "gos_interface_driver.h"
#include "stdio.h"
#include "register_map.h"

int main()
{
	void *hlsdev = getvaddr(0x43C00000);

    //Pulse wait request and reset
    *((int*)(hlsdev)+1) = 1;
    *((int*)(hlsdev)+6) = 1;
    *((int*)(hlsdev)+6) = 0;
    *((int*)(hlsdev)+1) = 0;

    //Start the op
    *((int*)(hlsdev)) = 1;
    *((int*)(hlsdev)) = 0;

    //block till finish
    while(*((int*)(hlsdev)+2) == 0){}
    //while(*((int*)(hlsdev)+3) != 46){}

    //check for errors
    if(*((int*)(hlsdev)+4) != 0){
        printf("\t%d, \t%d, \t%d, \t%d, \t%d, \t%d, \t%d, \tERROR\n", *((int*)(hlsdev)),*((int*)(hlsdev)+1),*((int*)(hlsdev)+2),*((int*)(hlsdev)+3),*((int*)(hlsdev)+4), *((int*)(hlsdev)+5), *((int*)(hlsdev)+6));
        //printf("CFG Error detected\n");
        return 1;
    }

    //printf("Circuit completed successfully ans=%d\n", *((int *)(hlsdev)+3));
    printf("\t%d, \t%d, \t%d, \t%d, \t%d, \t%d, \t%d, \tOKAY\n", *((int*)(hlsdev)),*((int*)(hlsdev)+1),*((int*)(hlsdev)+2),*((int*)(hlsdev)+3),*((int*)(hlsdev)+4), *((int*)(hlsdev)+5), *((int*)(hlsdev)+6));
	return 0;
}
