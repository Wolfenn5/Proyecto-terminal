/* Este codigo no forma parte del proyecto terminal, solo se utilizo para generar un archivo de extension .exe y poder realizar pruebas sobre el*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int proceso(char *binario);


int main()
{
	char *binario;
	int decimal;
	
	binario=(char*)malloc(10*sizeof(char));
	printf("Escribe un numero binario de 8 bits (unicamente unos y ceros sin espacio): ");
	fgets(binario,10,stdin);
	printf("\n"); 
	
	
	decimal= proceso(binario);
	
	
	if (decimal==0)
	{
		printf("El numero tiene uno o mas numeros mayores que uno, por favor utiliza unos y ceros unicamente");
	}
	else
	{
		printf("El numero binario %sen decimal es: %d", binario,decimal);
	}
	return 0;
}


int proceso(char *binario)
{
	int decimal=0;
	int potencia=1;
	int bandera=1;
	int i;
	
	i= strlen(binario)-1; // -1 por el enter
	
	while (i>=0 && bandera==1)
	{
		if (binario[i]>49) //Por codigo ascii el uno vale 49 y si es mayor quiere decir que hay un numero mayor que 1
		{
			bandera=0;
			decimal=0;
			return decimal;
		}
		else
		{
			if (binario[i]=='1')
			{
				decimal= decimal+1*potencia/2;
			}
			potencia= potencia*2;
			i--;
		}
	}
	return decimal;
}