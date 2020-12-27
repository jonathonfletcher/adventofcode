#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


#define NDROP   (3)
#define SMOL_ITERATIONS    (100)
#define HUGE_SIZE    (1000000)
#define HUGE_ITERATIONS (10000000)



void print_input_array(const int *input, int input_length, int input_offset)
{
    for ( int i=0 ; i < input_length ; i++ )
    {
        if (input_offset == i)
        {
            printf("(%d)", input[i]);
        } else {
            printf("%s%d%s", i==0?"":" ", input[i], i==input_length-1?"":" ");
        }
    }
    printf("\n");
}



int find_index(register int val, register int *input, register int input_length)
{
#if 1
register int i = 0;

    while (i < input_length)
    {
        if (val == *input)
        {
            return i;
        }

        i++;
        input++;
    }
#else
    for ( int i=0 ; i < input_length ; i++ )
    {
        if (val == input[i])
        {
            return i;
        }
    }
#endif
    return -1;
}



int find_dc(int val, int *drop_values, int minval, int maxval)
{
#if 1
    while (1)
    {
        val -= 1;
        if (val < minval) {
            val = maxval;
        }
        if (val != drop_values[0] && val != drop_values[1] && val != drop_values[2]) {
            return val;
        }
    }
#else
    val -= 1;

    if (val < minval)
        val = maxval;

    for ( int i=0 ; i < NDROP ; i++ )
    {
        if (val == drop_values[i])
        {
            return find_dc(val, drop_values, minval, maxval);
        }
    }

    return val;
#endif
}



void print_final_label(int *input, int input_length)
{
int one_index = find_index(1, input, input_length);

    for ( int i=1 ; i < input_length ; i++ )
    {
        printf("%d", input[(one_index+i)%input_length]);
    }
    printf("\n");
}



long long final_product(int *input, int input_length)
{
int one_index = find_index(1, input, input_length);

    printf("%ld * %ld\n", (long)input[(1+one_index)%input_length], (long)input[(2+one_index)%input_length]);
    return (long)input[(1+one_index)%input_length] * (long)input[(2+one_index)%input_length];
}



void update_circle(int *input, int offset, int input_length, int minval, int maxval, int *output)
{
int drop_values[NDROP];

    memcpy(output, input, input_length*sizeof(int));

    for ( register int i=0 ; i < NDROP ; i++ )
    {
        drop_values[i] = input[(offset+i+1)%input_length];
    }

    int dc = find_dc(input[offset], drop_values, minval, maxval);
    register int dc_offset = find_index(dc, input, input_length) - offset;
    dc_offset = ( dc_offset + input_length ) % input_length;
    // printf("dc: %d @ %d + %d\n", dc, offset, dc_offset);

    for ( register int i=input_length ; i < input_length+dc_offset-NDROP ; i++ )
    {
        int oi = i+1+NDROP;
        int ni = i+1;
        // printf("%d + %d -> %d + %d\n", offset, oi, offset, ni);
        output[(offset+ni)%input_length] = input[(offset+oi)%input_length];
    }

    for ( register int i=0 ; i < NDROP ; i++ )
    {
        int oi = i+1;
        int ni = dc_offset+input_length-2+i;
        // printf("%d + %d -> %d + %d\n", offset, oi, offset, ni%input_length);
        output[(offset+ni)%input_length] = input[(offset+oi)%input_length];
    }

}



int *make_input_array(const char *input_str, const int input_length)
{
int *input_array = NULL;
int maxval = -1;

    // printf("%s %d\n", input_str, input_length);
    input_array = calloc(input_length, sizeof(int));
    for ( int i=0 ; i < strlen(input_str) ; i++ )
    {
        input_array[i] = input_str[i] - 48;
        if (input_array[i] > maxval)
        {
            maxval = input_array[i];
        }
    }
    for ( int i=strlen(input_str) ; i < input_length ; i++ )
    {
        maxval = maxval+1;
        input_array[i] = maxval;
    }

    return input_array;
}



void run(const char *input_str, int huge)
{
const int input_length = huge ? HUGE_SIZE : strlen(input_str);
register int *input_array = make_input_array(input_str, input_length);
register int *output_array = make_input_array(input_str, input_length);
register int *tmp_array;
int offset = 0;
int minval, maxval;
int iterations = huge ? HUGE_ITERATIONS : SMOL_ITERATIONS;
time_t start_time, current_time;

    minval = 1;
    maxval = input_length;

    // printf("%d (%d, %d)\n", input_length, minval, maxval);

    start_time = time(NULL);
    for ( int j=0 ; j < iterations ; j++ )
    {
        if (huge && j > 0 && j % 1000 == 0 )
        {
            current_time = time(NULL);
            printf("%d / %d (%.0f%%)\n", j, iterations, 100.*j/iterations);
            printf("%lds elapsed / %.0lfs remaining\n", (long)current_time-start_time, (double)((current_time-start_time)/(1.*j/iterations)-(current_time-start_time)));
        }

        update_circle(input_array, offset, input_length, minval, maxval, output_array);
        tmp_array = input_array; input_array = output_array ; output_array = tmp_array;

        offset = (offset+1)%input_length;
    }

    if (huge)
    {
        current_time = time(NULL);
        printf("%lds total\n", (long)current_time-start_time);
        printf("%lld\n", final_product(input_array, input_length));
    } else {
        print_input_array(input_array, input_length, offset);
        print_final_label(input_array, input_length);
    }

    free(output_array);
    free(input_array);
}



int main(int argc, char **argv)
{
const char *input_str = "389125467";

    run(input_str, 0);
    run(input_str, 1);

    return EXIT_SUCCESS;
}


